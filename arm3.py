import tkinter as tk
import math

WIDTH = 900
HEIGHT = 700
DRAW_HEIGHT = 400

ORIGIN_X = 200
ORIGIN_Y = 300

STEP_EXTEND = 3
STEP_ROTATE = math.radians(2)

vectors = []

preview_len = 0
extending = False
rot_dir = 0
selected_joint = None

root = tk.Tk()
root.title("Manipulator Matrix Visualizer")

canvas = tk.Canvas(root,width=WIDTH,height=DRAW_HEIGHT,bg="white")
canvas.pack()

formula_label = tk.Label(root,font=("Courier",16),justify="left")
formula_label.pack(fill="both",expand=True)


def compute_points():

    pts=[(0,0)]

    x=0
    y=0
    angle_sum=0

    for length,angle in vectors:

        angle_sum+=angle

        x+=length*math.cos(angle_sum)
        y+=length*math.sin(angle_sum)

        pts.append((x,y))

    return pts


def draw():

    canvas.delete("all")

    pts=compute_points()

    screen=[]

    for x,y in pts:

        sx=ORIGIN_X+x
        sy=ORIGIN_Y-y

        screen.append((sx,sy))


    # 점 사이 검정 선
    for i in range(len(screen)-1):

        x1,y1=screen[i]
        x2,y2=screen[i+1]

        canvas.create_line(x1,y1,x2,y2,width=4,fill="black")


    # 점 표시
    for i,(x,y) in enumerate(screen):

        color="black"

        if selected_joint==i:
            color="red"

        canvas.create_oval(x-5,y-5,x+5,y+5,fill=color)


    # 연장 미리보기
    if extending:

        canvas.create_line(
            ORIGIN_X,
            ORIGIN_Y,
            ORIGIN_X+preview_len,
            ORIGIN_Y,
            dash=(5,3),
            fill="green",
            width=3
        )


def build_formula():

    top=""
    bottom=""

    for i,(length,angle) in enumerate(vectors):

        idx=i+1

        cos_term=f"C{''.join(str(j) for j in range(1,idx+1))}"
        sin_term=f"S{''.join(str(j) for j in range(1,idx+1))}"

        top+=f"[{cos_term}  -{sin_term}][{length:.1f}]"
        bottom+=f"[{sin_term}   {cos_term}][ 0 ]"

        if i<len(vectors)-1:

            top+=" + "
            bottom+="   "

    formula_label.config(text=top+"\n"+bottom)


def extend_start(e):

    global extending
    extending=True


def extend_stop(e):
    pass


def confirm():

    global preview_len,extending

    if preview_len<5:
        return

    vectors.insert(0,(preview_len,0))

    preview_len=0
    extending=False

    build_formula()


def rotate_pos(e):

    global rot_dir
    rot_dir=1


def rotate_neg(e):

    global rot_dir
    rot_dir=-1


def rotate_stop(e):

    global rot_dir
    rot_dir=0


def rotate_chain():

    if selected_joint is None:
        return

    if selected_joint>=len(vectors):
        return

    l,a=vectors[selected_joint]

    vectors[selected_joint]=(l,a+rot_dir*STEP_ROTATE)


def update():

    global preview_len

    if extending:
        preview_len+=STEP_EXTEND

    if rot_dir!=0:
        rotate_chain()
        build_formula()

    draw()

    root.after(16,update)


def select_point(event):

    global selected_joint

    pts=compute_points()

    for i,(x,y) in enumerate(pts):

        sx=ORIGIN_X+x
        sy=ORIGIN_Y-y

        if math.hypot(event.x-sx,event.y-sy)<10:

            selected_joint=i
            break


canvas.bind("<Button-1>",select_point)


frame=tk.Frame(root)
frame.pack()

btn1=tk.Button(frame,text="연장")
btn1.grid(row=0,column=0,padx=10)

btn1.bind("<ButtonPress-1>",extend_start)
btn1.bind("<ButtonRelease-1>",extend_stop)

btn2=tk.Button(frame,text="확정",command=confirm)
btn2.grid(row=0,column=1,padx=10)

btn3=tk.Button(frame,text="회전 +")
btn3.grid(row=0,column=2,padx=10)

btn3.bind("<ButtonPress-1>",rotate_pos)
btn3.bind("<ButtonRelease-1>",rotate_stop)

btn4=tk.Button(frame,text="회전 -")
btn4.grid(row=0,column=3,padx=10)

btn4.bind("<ButtonPress-1>",rotate_neg)
btn4.bind("<ButtonRelease-1>",rotate_stop)


build_formula()
update()

root.mainloop()