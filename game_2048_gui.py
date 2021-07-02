import numpy as np
import random
import tkinter


key = ""
def key_down(event):
    global key
    key = event.keysym

def key_up(event):
    global key
    key = ""

def trans_key(s):
    if s == "Up":
        return "u"
    if s == "Down":
        return "d"
    if s == "Left":
        return "l"
    if s == "Right":
        return "r"

class game_2048:
    def __init__(self):
        self.state = np.zeros((4,4))
        x = [ random.randint(0,3),  random.randint(0,3) ]
        y = [ random.randint(0,3),  random.randint(0,3) ]
        for i in [0,1]:
            if x[i] == y[i]:
                while True:
                    x[i] = random.randint(0,3)
                    if x[i] != y[i]:
                            break

        self.state[x[0], x[1]] = 2*random.randint(1,2)
        self.state[y[0], y[1]] = 2*random.randint(1,2)
        self.action = {"t":0, "d":1, "l":2, "r":3}
        
        self.flag_finish = True
        self.flag_step = True
        
    def calc_next_state(self, state):
        next_state = np.zeros((4,4))

        for i in range(4):
            col = state[ : , i ]
            tmp = col[col > 0]
            next_state[ : len(tmp) , i ] = tmp

            lst = []
            forbidden_lst = []
            next_state_tmp = np.hstack([next_state[ :  , i ], np.array(0)])
            tmp = np.zeros(4)
            for j in range(4):
                if j not in forbidden_lst:
                    if next_state_tmp[ j + 1 ] == next_state_tmp[ j ]:
                        lst.append(2 * next_state_tmp[ j ])
                        forbidden_lst.append( j + 1 )
                    else:
                        lst.append(next_state_tmp[ j ])
            tmp[:len(lst)] = np.array(lst)
            next_state[ : , i ] = tmp


        return next_state
        
        
    def get_next_state(self, action):
        self.flag_step = True
        past_state = self.state.copy()
        
        state_u = self.calc_next_state(self.state.copy())
        
        tmp = np.flipud(self.state.copy())
        state_d = np.flipud(self.calc_next_state(tmp))
        
        tmp = np.rot90(self.state, -1)
        state_l = np.rot90(self.calc_next_state(tmp), 1)
        
        tmp = np.rot90(self.state, 1)
        state_r = np.rot90(self.calc_next_state(tmp), -1)
        
        if np.all(state_u==past_state) and np.all(state_d==past_state) and np.all(state_l==past_state) and np.all(state_r==past_state):
            self.flag_finish = False
            print("game over")
            return
        if action =="" or action == None:
            return
        if action == "u":
            if np.all(state_u==past_state):
                #print("input other direction")
                #print("======================================================================================")
                self.flag_step = False
                return
            else:
                self.state = state_u
        elif action == "d":
            if np.all(state_d==past_state):
                #print("input other direction")
                #print("======================================================================================")
                self.flag_step = False
                return
            else:
                self.state = state_d
        elif action == "l":
            if np.all(state_l==past_state):
                #print("input other direction")
                #print("======================================================================================")
                self.flag_step = False
                return
            else:
                self.state = state_l
        else:
            if np.all(state_r==past_state):
                #print("input other direction")
                #print("======================================================================================")
                self.flag_step = False
                return
            else:
                self.state = state_r
        
        while True:
            x = [ random.randint(0,3),  random.randint(0,3) ]
            if self.state[x[0],x[1]] == 0:
                self.state[x[0],x[1]] = 2*random.randint(1,2)
                break
            else:
                continue
                
game = game_2048()

root = tkinter.Tk()
root.title("2048")
root.bind("<KeyPress>",key_down)
root.bind("<KeyRelease>", key_up)

canvas = tkinter.Canvas(width = 800, height = 800, bg="white")
canvas.pack()


for i in range(4):
    for j in range(4):
        if game.state[i][j] != 0:
            canvas.create_rectangle(200*j,200*i,200*(j+1), 200*(i+1), fill = "orange",tag = "num_block")
            canvas.create_text( 100 + 200 * j,  100 + 200 * i, text = int(game.state[i][j]), fill = "black", tag = "num_block")


for i in range(3):
    canvas.create_line( 200 * (i+1), 0, 200 * (i+1), 800 )
    canvas.create_line(0,  200 * (i+1), 800, 200 * (i+1))

        
def main_process():
    global key
    canvas.delete("num_block")
    
    game.get_next_state(trans_key(key))
    
    for i in range(4):
        for j in range(4):
            if game.state[i][j] != 0:
                canvas.create_rectangle(200*j,200*i,200*(j+1), 200*(i+1), fill = "orange",tag = "num_block")
                canvas.create_text( 100 + 200 * j,  100 + 200 * i, text = int(game.state[i][j]), fill = "black", tag = "num_block", font = ("",50))
                
                
    root.after(100, main_process)

    
    
main_process()
root.mainloop()
