import turtle
import pandas

screen = turtle.Screen()
screen.title("US States Game")
image = "blank_states_img.gif"
screen.addshape(image)
turtle.shape(image)
countries_entered = []
data = pandas.read_csv("50_states.csv")
states = data["state"].to_list()

length = len(states)
US_state = 0

while len(countries_entered) < 50:
    answer_state = screen.textinput(title=f"Guess the state {US_state}/{length }",
                                    prompt="What's another state's name?").title()
    state_data = data[data["state"] == answer_state]
    if answer_state == "Exit":
        states_to_learn = [state for state in states if state not in countries_entered]
        df = pandas.DataFrame(states_to_learn)
        df.to_csv("states_to_learn.csv")

        break
    if answer_state in states and answer_state not in countries_entered:
        state_writer = turtle.Turtle()
        state_writer.hideturtle()
        state_writer.penup()
        state_writer.goto(int(state_data.x), int(state_data.y))
        state_writer.write(answer_state, align="center", font=("Arial", 10, "normal"))
        state_writer.pendown()
        countries_entered.append(answer_state)
        US_state += 1

