#import csv
# with open("weather_data.csv")as file:
    # data = csv.reader(file)
    # temperature = []
    # for row in data:
        # if row[1] != "temp":
            # temperature.append(int(row[1]))
    # print(temperature)
# import pandas
# data = pandas.read_csv("weather_data.csv")
# print(data["temp"])
#data_dict = data.to_dict()
#print(data_dict)
# temp_list = data["temp"].max()
# print(temp_list)
# print(data[data.day == "Monday"])
# print(data[data.temp == data["temp"].max()])

# monday = data[data.day == "Monday"]
# print(monday.temp * (9/5)+ 32)
#
# # creating dataframes
# data_dict = {
#     "students": ["Fab", "Liha", "Angie"],
#     "scores": [60, 70, 80]
# }
# data = pandas.DataFrame(data_dict)
# print(data)
# data.to_csv("scores.csv")
import pandas
data = pandas.read_csv("squirrel.csv")
# print(data["Primary Fur Color"])
black_count = len(data[data["Primary Fur Color"] == "Black"])
red_count = len(data[data["Primary Fur Color"] == "Cinnamon"])
gray_count = len(data[data["Primary Fur Color"] == "Gray"])
colour_dict = {
    "Fur Colour": ["gray", "red", "black"],
    "Count": [gray_count, red_count, black_count]
}
data = pandas.DataFrame(colour_dict)
print(data)
data.to_csv("squirrel_count.csv")