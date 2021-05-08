#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Import libraries used for this program
# a basic graphic library
import turtle

def pad_a_up():
    y = pad_a.ycor()
    y += 20
    pad_a.sety(y)   

def pad_a_down():
    y = pad_a.ycor()
    y -= 20
    pad_a.sety(y)

def pad_b_up():
    y = pad_b.ycor()
    y += 20
    pad_b.sety(y)   

def pad_b_down():
    y = pad_b.ycor()
    y -= 20
    pad_b.sety(y)  

def main():

    win = turtle.Screen()
    win.title("A PING-PONG Game")
    win.bgcolor('black')
    win.setup(width=800,height=600)
    win.tracer(0)

    #Left Pad
    pad_a= turtle.Turtle()
    pad_a.speed(0)
    pad_a.shape("square")
    pad_a.color("blue")
    pad_a.shapesize(stretch_wid=5,stretch_len=1)
    pad_a.penup()
    pad_a.goto(-350,0)

    # Right Pad
    pad_b= turtle.Turtle()
    pad_b.speed(0)
    pad_b.shape("square")
    pad_b.color("red")
    pad_b.shapesize(stretch_wid=5,stretch_len=1)
    pad_b.penup()
    pad_b.goto(350,0)

    # Ball
    ball= turtle.Turtle()
    ball.speed(1000)
    ball.shape("square")
    ball.color("white")
    ball.penup()
    ball.goto(0,0)
    ball.dx = 0.05
    ball.dy = 0.05

    # Score
    score_a = 0
    score_b = 0

    # score context
    pen = turtle.Turtle()
    pen.speed(0)
    pen.color("white")
    pen.penup()
    pen.hideturtle()
    pen.goto(0,260)
    pen.write("Player A : "+ str(score_a) +" Player B : "+ str(score_b),align="center",font=("Courier",24,"normal"))


    win.listen()
    win.onkeypress(pad_a_up,"w")
    win.onkeypress(pad_a_down,"s")
    win.onkeypress(pad_b_up,"Up")
    win.onkeypress(pad_b_down,"Down")

    while True:
        win.update()
        ball.setx(ball.xcor() + ball.dx)
        ball.sety(ball.ycor() + ball.dy)

        if ball.ycor() > 290 :
            ball.sety(290)
            ball.dy *= -1

        if ball.ycor() < -290 :
            ball.sety(-290)
            ball.dy *= -1

        if ball.xcor() > 390 :
            score_a += 1
            ball.goto(0,0)
            ball.dx *= -1
            pen.clear()
            pen.write("Player A : "+ str(score_a) +" Player B : "+ str(score_b),align="center",font=("Courier",24,"normal"))

        if ball.xcor() < -390 :
            score_b += 1
            ball.goto(0,0)
            ball.dx *= -1
            pen.clear()
            pen.write("Player A : "+ str(score_a) +" Player B : "+ str(score_b),align="center",font=("Courier",24,"normal"))


        if (ball.xcor() > 340 and ball.xcor() < 350) and ball.ycor() < pad_b.ycor() + 50 and ball.ycor() > pad_b.ycor() - 50 :
            ball.setx(340)
            ball.dx *= -1

        if (ball.xcor() < -340 and ball.xcor() > -350) and ball.ycor() < pad_a.ycor() + 50 and ball.ycor() > pad_a.ycor() - 50 :
            ball.setx(-340)
            ball.dx *= -1
            
if __name__ == '__main__':
    main()


# In[ ]:





# In[ ]:




