import random  # Import the random module for random number generation
import pygame  # Import the pygame module for game development
from pygame.locals import *  # Import all pygame local variables
from actors import *  # Import all classes and functions from the actors module

# Global variables dictionary
g_vars = {}
g_vars['width'] = 800  # Width of the game window
g_vars['height'] = 850  # Height of the game window
g_vars['fps'] = 30  # Frames per second
g_vars['grid'] = 32  # Size of the grid in pixels
g_vars['window'] = pygame.display.set_mode([g_vars['width'], g_vars['height']], pygame.HWSURFACE)  # Create the game window

class App:
    def __init__(self):
        pygame.init()  # Initialize pygame
        pygame.display.set_caption("Frogger")  # Set the window caption
        
        self.running = None  # Initialize running state
        self.state = None  # Initialize game state
        self.frog = None  # Initialize frog object
        self.score = None  # Initialize score object
        self.lanes = None  # Initialize lanes list

        self.clock = pygame.time.Clock()  # Initialize game clock
        self.font = pygame.font.SysFont('Courier New', 16)  # Initialize font for text

    def init(self):
        self.running = True  # Set running state to True
        self.state = 'START'  # Set initial game state to 'START'
        
        # Initialize frog at the center bottom of the screen
        self.frog = Frog(g_vars['width'] / 2 - g_vars['grid'] / 2, 24 * g_vars['grid'], g_vars['grid'])
        self.frog.attach(None)  # Attach frog to no object
        self.score = Score()  # Initialize score

        self.lanes = []  # Initialize lanes list
        # Add lanes to the game
        self.lanes.append(Lane(1, c=(50, 192, 122)))
        self.lanes.append(Lane(2, t='log', c=(153, 217, 234), n=2, l=6, spc=350, spd=5))
        self.lanes.append(Lane(3, t='log', c=(153, 217, 234), n=3, l=2, spc=180, spd=-4))
        self.lanes.append(Lane(4, t='log', c=(153, 217, 234), n=4, l=2, spc=140, spd=4))
        self.lanes.append(Lane(5, t='log', c=(153, 217, 234), n=2, l=3, spc=230, spd=-3))
        self.lanes.append(Lane(6, c=(50, 192, 122)))
        self.lanes.append(Lane(7, c=(50, 192, 122)))
        self.lanes.append(Lane(8, t='car', c=(195, 195, 195), n=3, l=2, spc=180, spd=-4))
        self.lanes.append(Lane(9, t='car', c=(195, 195, 195), n=2, l=4, spc=240, spd=-3))
        self.lanes.append(Lane(10, t='car', c=(195, 195, 195), n=4, l=2, spc=130, spd=2.5))
        self.lanes.append(Lane(11, t='car', c=(195, 195, 195), n=3, l=3, spc=200, spd=3))
        self.lanes.append(Lane(12, c=(50, 192, 122)))
        self.lanes.append(Lane(13, c=(50, 192, 122)))
        self.lanes.append(Lane(14, t='log', c=(153, 217, 234), n=2, l=6, spc=350, spd=2))
        self.lanes.append(Lane(15, t='log', c=(153, 217, 234), n=3, l=2, spc=180, spd=-1.6))
        self.lanes.append(Lane(16, t='log', c=(153, 217, 234), n=4, l=2, spc=140, spd=1.6))
        self.lanes.append(Lane(17, t='log', c=(153, 217, 234), n=2, l=3, spc=230, spd=-2))
        self.lanes.append(Lane(18, c=(50, 192, 122)))
        self.lanes.append(Lane(19, c=(50, 192, 122)))
        self.lanes.append(Lane(20, t='car', c=(195, 195, 195), n=3, l=2, spc=180, spd=-2))
        self.lanes.append(Lane(21, t='car', c=(195, 195, 195), n=2, l=4, spc=240, spd=-1))
        self.lanes.append(Lane(22, t='car', c=(195, 195, 195), n=4, l=2, spc=130, spd=2.5))
        self.lanes.append(Lane(23, t='car', c=(195, 195, 195), n=3, l=3, spc=200, spd=1))
        self.lanes.append(Lane(24, c=(50, 192, 122)))

    def event(self, event):
        if event.type == QUIT:  # If the event is QUIT
            self.running = False  # Set running state to False

        if event.type == KEYDOWN and event.key == K_ESCAPE:  # If the event is pressing the ESC key
            if self.state == 'PLAYING':  # If the game state is 'PLAYING'
                self.state = 'PAUSE'  # Change the state to 'PAUSE'
            elif self.state == 'PAUSE':  # If the game state is 'PAUSE'
                self.state = 'PLAYING'  # Change the state to 'PLAYING'

        if self.state == 'START':  # If the game state is 'START'
            if event.type == KEYDOWN and event.key == K_RETURN:  # If the event is pressing the ENTER key
                self.state = 'PLAYING'  # Change the state to 'PLAYING'

        if self.state == 'PLAYING':  # If the game state is 'PLAYING'
            if event.type == KEYDOWN and event.key == K_LEFT:  # If the event is pressing the LEFT arrow key
                self.frog.move(-1, 0)  # Move the frog left
            if event.type == KEYDOWN and event.key == K_RIGHT:  # If the event is pressing the RIGHT arrow key
                self.frog.move(1, 0)  # Move the frog right
            if event.type == KEYDOWN and event.key == K_UP:  # If the event is pressing the UP arrow key
                self.frog.move(0, -1)  # Move the frog up
            if event.type == KEYDOWN and event.key == K_DOWN:  # If the event is pressing the DOWN arrow key
                self.frog.move(0, 1)  # Move the frog down

        if self.state == 'PAUSE':  # If the game state is 'PAUSE'
            if event.type == KEYDOWN:  # If a key is pressed
                if event.key == K_r:  # If the key is 'R'
                    self.reset_game()  # Reset the game
                    self.state = 'PLAYING'  # Change the state to 'PLAYING'
                if event.key == K_m:  # If the key is 'M'
                    self.state = 'START'  # Change the state to 'START'

    def reset_game(self):
        self.frog.reset()  # Reset frog's position
        self.score.lives = 3  # Reset lives to initial value
        self.score.score = 0  # Optionally reset score

    def update(self):
        if self.state == 'PLAYING':  # If the game state is 'PLAYING'
            for lane in self.lanes:  # Update each lane
                lane.update()
            
            lane_index = self.frog.y // g_vars['grid'] - 1  # Calculate the lane index of the frog
            if self.lanes[lane_index].check(self.frog):  # Check for collision in the current lane
                self.score.lives -= 1  # Decrease lives by 1
                self.score.score = 0  # Reset score to 0
            
            self.frog.update()  # Update frog's state

            # Update score and high_lane if frog moves to a higher lane
            if (g_vars['height'] - self.frog.y) // g_vars['grid'] > self.score.high_lane:
                if self.score.high_lane == 24:  # If the frog reached the highest lane
                    self.frog.reset()  # Reset frog's position
                    self.score.update(200)  # Update score by 200
                else:
                    self.score.update(10)  # Update score by 10
                    self.score.high_lane = (g_vars['height'] - self.frog.y) // g_vars['grid']  # Update high_lane

            if self.score.lives == 0:  # If lives are 0
                self.frog.reset()  # Reset frog's position
                self.score.reset()  # Reset score
                self.state = 'START'  # Change the state to 'START'
                
            if self.score.score >= 1000:  # If score is 1000 or more
                self.state = 'CONGRATULATIONS'  # Change the state to 'CONGRATULATIONS'

    def draw(self):
        g_vars['window'].fill((0, 0, 0))  # Fill the window with black color
        if self.state == 'START':  # If the game state is 'START'
            self.draw_text("Look B4U Cross!", g_vars['width'] / 2, g_vars['height'] / 2 - 15, 'center')
            self.draw_text("Press ENTER to start playing.", g_vars['width'] / 2, g_vars['height'] / 2 + 15, 'center')

        if self.state == 'PLAYING':  # If the game state is 'PLAYING'
            self.draw_text("Lives: {0}".format(self.score.lives), 5, 8, 'left')  # Draw lives
            self.draw_text("Score: {0}".format(self.score.score), 120, 8, 'left')  # Draw score
            self.draw_text("High Score: {0}".format(self.score.high_score), 240, 8, 'left')  # Draw high score

            for lane in self.lanes:  # Draw each lane
                lane.draw()
            self.frog.draw()  # Draw the frog

        if self.state == 'PAUSE':  # If the game state is 'PAUSE'
            self.draw_text("Paused", g_vars['width'] / 2, g_vars['height'] / 2 - 30, 'center')  # Draw pause message
            self.draw_text("Press R to reset", g_vars['width'] / 2, g_vars['height'] / 2, 'center')  # Draw reset message
            self.draw_text("Press M to return to main menu", g_vars['width'] / 2, g_vars['height'] / 2 + 30, 'center')  # Draw main menu message
        
        if self.state == 'CONGRATULATIONS':  # If the game state is 'CONGRATULATIONS'
            self.draw_text("Congratulations!", g_vars['width'] / 2, g_vars['height'] / 2 - 30, 'center')  # Draw congratulations message
            self.draw_text("You are road safe.", g_vars['width'] / 2, g_vars['height'] / 2, 'center')  # Draw road safe message
            self.draw_text("Press ENTER to restart", g_vars['width'] / 2, g_vars['height'] / 2 + 30, 'center')  # Draw restart message

        pygame.display.flip()  # Update the display

    def draw_text(self, t, x, y, a):
        text = self.font.render(t, False, (255, 255, 255))  # Render the text
        if a == 'center':  # If alignment is center
            x -= text.get_rect().width / 2  # Center the text horizontally
        elif a == 'right':  # If alignment is right
            x += text.get_rect().width  # Align the text to the right
        g_vars['window'].blit(text, [x, y])  # Draw the text on the window

    def cleanup(self):
        pygame.quit()  # Quit pygame
        quit()  # Exit the program

    def execute(self):
        if self.init() == False:  # If initialization fails
            self.running = False  # Set running state to False
        while self.running:  # Main game loop
            for event in pygame.event.get():  # Process events
                self.event(event)  # Handle events
                if self.state == 'CONGRATULATIONS' and event.type == KEYDOWN and event.key == K_RETURN:  # If in 'CONGRATULATIONS' state and ENTER is pressed
                    self.reset_game()  # Reset the game
                    self.state = 'START'  # Change the state to 'START'
            self.update()  # Update game state
            self.draw()  # Draw game state
            self.clock.tick(g_vars['fps'])  # Cap the frame rate
        self.cleanup()  # Clean up resources

if __name__ == "__main__":
    gameApp = App()  # Create game app instance
    gameApp.execute()  # Execute the game
