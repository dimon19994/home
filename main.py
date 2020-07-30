from flask import Flask, render_template, request, url_for, redirect, send_from_directory
from werkzeug.utils import secure_filename
import os
from copy import deepcopy

app = Flask(__name__)


def toint(liste):
    for i in range(len(liste)):
        for j in range(len(liste[i])):
            liste[i][j] = int(liste[i][j])
    return liste

def delete_space(liste, string):
    del liste[0]
    for i in range(len(liste)):
        for j in range(len(liste[i])):
            if int(liste[i][j]) in string:
                liste[i][j] = " "
            else:
                liste[i][j] = int(liste[i][j])

    liste = list(zip(*liste))

    for i in range(len(liste)):
        liste[i] = list(filter(lambda x: x != " ", liste[i]))
        for j in range(15 - len(liste[i]) - 1):
            liste[i].insert(0, 0)

    liste = list(zip(*liste))

    for i in range(len(liste)):
        liste[i] = list(liste[i])

    return liste


@app.route("/", methods=['GET', 'POST'])
def root():
    return render_template('index.html')


@app.route("/ststistic/<type>/<year>", methods=['GET', 'POST'])
@app.route("/ststistic/<type>", methods=['GET', 'POST'])
def ststistic(type, year = None):
    if year == "last":
        files = os.listdir("templates/statistic_"+type)[:-1]
        full_list = [os.path.join("templates/statistic_"+type, i) for i in files]
        time_sorted_list = max(full_list, key=os.path.getmtime)
        res = time_sorted_list.split("\\")
        res = res[1].split(".")[0]
    else:
        res = year
    return render_template("statistic_"+type+"/"+res+".html", year = res)


@app.route("/result/<type>", methods=['GET', 'POST'])
def result(type):
    files = os.listdir("data_"+type)
    full_list = [os.path.join("data_"+type, i) for i in files]
    time_sorted_list = max(full_list, key=os.path.getmtime)
    print(time_sorted_list)
    res = time_sorted_list.split("\\")
    res = res[1].split(".")

    return redirect(url_for('show', type=type, filename=res[0]))


@app.route("/show/<type>/<filename>", methods=['GET', 'POST'])
def show(type, filename):

    f = open("data_"+ type +"/"+filename + ".txt", "r")
    text = f.read()
    f.close()

    text = text.split("\n")
    for i in range(len(text)):
        text[i] = text[i].split(",")

    date = text[0][0]
    text_1_1 = text[1:16]
    text_1_2 = text[16:31]

    text_2_1 = text[31:46]
    text_2_2 = text[46:61]
    form_string = text[-2]

    return render_template("show.html", list_1 = [text_1_1, text_1_2], list_2 = [text_2_1, text_2_2], string = form_string, date= date,  number = filename)


@app.route("/keno_one", methods=['GET', 'POST'])
def keno_one():
    if request.method == 'POST':
        form_data = request.form

        form_string = form_data["numbers"].split(" ")[:-1]
        for i in range(len(form_string)):
            form_string[i] = int(form_string[i])

        f = open("data_keno/"+str(int(form_data["number_game"])-1)+".txt", "r")
        text = f.read()
        f.close()

        text = text.split("\n")
        for i in range(len(text)):
            text[i] = text[i].split(",")

        date = form_data["date"]

        text_2_1 = text[31:46]
        text_2_2 = text[46:61]

        text_2_1_c = deepcopy(text_2_1)
        text_2_2_c = deepcopy(text_2_2)

        text_2_1_n = delete_space(text_2_1_c, form_string)
        text_2_1_n.append(form_string)

        form_string_sort = deepcopy(form_string)
        form_string_sort.sort()
        text_2_2_n = delete_space(text_2_2_c, form_string_sort)
        text_2_2_n.append(form_string_sort)

        f = open("data_keno/"+form_data["number_game"] + ".txt", "w")
        f.write(date+"\n")
        for i in [text_2_1, text_2_2, text_2_1_n, text_2_2_n]:
            for j in i:
                for k in range(len(j)-1):
                    f.write(str(j[k])+",")
                f.write(str(j[-1])+"\n")
        f.close()

        try:
            f = open("templates/analis/"+form_data["date"].split("-")[0]+".html", "r")
        except:
            f = open("templates/analis/" + form_data["date"].split("-")[0] + ".html", "w")
            f.write("{% extends 'analis/analis_index.html' %}\n{% block year %}\n\t<table>\n\t<tr><td>Data</td><td>Sozv/Grad</td><td>d/l</td><td>0 pr</td><td>Po vipad</td><td>Podryad</td><td>Luna b/k</td><td></td></tr></table>\t{% endblock %}")
            f.close()
            f = open("templates/analis/" + form_data["date"].split("-")[0] + ".html", "r")

        text = f.read()
        f.close()

        count_0 = 0
        for i in form_string:
            if str(i) in text_2_1[-1]:
                count_0 += 1

        list_of_thtow = []
        for i in range(len(form_string)):
            if int(text_2_1[-1][i]) in form_string:
                list_of_thtow.append(str(i+1))


        list_of_thtow_sort = []
        for i in range(len(form_string)):
            if int(text_2_2[-1][i]) in form_string:
                list_of_thtow_sort.append(str(i+1))


        new_string = "<tr><td>"+form_data["date"]+"</td>"

        for i in range(2, 9):
            if i == 4:
                new_string += "<td>"+str(count_0)+"</td>"
            elif i == 5:
                new_string += "<td>"+" ".join(list_of_thtow)+"</td>"
            elif i == 6:
                new_string += "<td>"+" ".join(list_of_thtow_sort)+"</td>"
            else:
                new_string += "<td></td>"
        
        new_string += "</tr>"

        text_new = text.split("</table>")
        text_new[0]+=new_string
        join_text_new = "</table>".join(text_new)
        f = open("templates/analis/"+form_data["date"].split("-")[0]+".html", "w")
        f.write(join_text_new)
        f.close()

        try:
            f = open("templates/statistic_keno/"+form_data["date"].split("-")[0]+".html", "r")
        except:
            f = open("templates/statistic_keno/" + form_data["date"].split("-")[0] + ".html", "w")
            f.write("{% extends 'statistic_keno/statistic_index.html' %}\n{% block year %}\n\t<table>\n\t</table>\t{% endblock %}")
            f.close()
            f = open("templates/statistic_keno/" + form_data["date"].split("-")[0] + ".html", "r")

        data = f.read()
        f.close()
        data = data.split("</table>")

        row = ""
        row1 = ""
        row2 = ""
        row += "<tr>\n\t\t\t<td style = 'width: 250px'>"+form_data["date"]+"</td>\n"

        for i in range(1, 81):
            if i in form_string:
                if i % 10 == 1:
                    row += "\t\t\t<td style = 'background-color: pink; border-left: 3px solid black'></td>\n"
                else:
                    row += "\t\t\t<td style = 'background-color: pink'></td>\n"
            else:
                if i % 10 == 1:
                    row += "\t\t\t<td style = 'border-left: 3px solid black'></td>\n"
                else:
                    row += "\t\t\t<td></td>\n"
        row += "\t\t</tr>\n"

        if form_data["date"].split("-")[2] == "01" or form_data["date"].split("-")[2] == "15":
            row1 += "<tr>\n\t\t\t<td style = 'width: 250px'></td>\n"
            row2 += "<tr>\n\t\t\t<td style = 'width: 250px'></td>\n"

            for i in range(0, 9):
                for j in range(0, 10):
                    if (i == 0 and j == 0) or (i == 8 and j != 0):
                        continue
                    else:
                        if j % 10 == 1:
                            row1 += "\t\t\t<td style = 'background-color: green; border-left: 3px solid black'>" + str(i) + "</td>\n"
                            row2 += "\t\t\t<td style = 'background-color: green; border-left: 3px solid black'>" + str(j) + "</td>\n"
                        else:
                            row1 += "\t\t\t<td style = 'background-color: green'>" + str(i) + "</td>\n"
                            row2 += "\t\t\t<td style = 'background-color: green'>" + str(j) + "</td>\n"
            row1 += "\t\t</tr>\n"
            row2 += "\t\t</tr>\n"
            data[0] = data[0] + row1 + row2 + row + "\t\t</table>" + data[1]
        else:
            data[0] = data[0] + row + "\t\t</table>" + data[1]

        f = open("templates/statistic_keno/"+form_data["date"].split("-")[0]+".html", "w")
        f.write(data[0])
        f.close()

        return redirect(url_for('show', type = "keno", filename=form_data["number_game"]))

    return render_template('keno_one.html')


@app.route("/keno_many", methods=['GET', 'POST'])
def keno_many():
    if request.method == 'POST':
        file = request.files["file_name"]
        filename = secure_filename(file.filename)
        file.save(os.path.join("sours_keno/", filename))

        f = open("sours_keno/"+filename)
        data = f.read()
        data = data.split("\n")[1:-1]
        for i in range(len(data)):
            data[i] = data[i].split("\t")[:2] + data[i].split("\t")[4:24]

        data.reverse()
        for d in range(len(data)):
            form_string = data[d][2:]
            for i in range(len(form_string)):
                form_string[i] = int(form_string[i])

            f = open("data_keno/" + str(int(data[d][0]) - 1) + ".txt", "r")
            text = f.read()
            f.close()

            text = text.split("\n")
            for i in range(len(text)):
                text[i] = text[i].split(",")

            date = data[d][1]

            text_2_1 = text[31:46]
            text_2_2 = text[46:61]

            text_2_1_c = deepcopy(text_2_1)
            text_2_2_c = deepcopy(text_2_2)

            text_2_1_n = delete_space(text_2_1_c, form_string)
            text_2_1_n.append(form_string)

            form_string_sort = deepcopy(form_string)
            form_string_sort.sort()
            text_2_2_n = delete_space(text_2_2_c, form_string_sort)
            text_2_2_n.append(form_string_sort)

            f = open("data_keno/" + data[d][0] + ".txt", "w")
            f.write(date + "\n")
            for i in [text_2_1, text_2_2, text_2_1_n, text_2_2_n]:
                for j in i:
                    for k in range(len(j) - 1):
                        f.write(str(j[k]) + ",")
                    f.write(str(j[-1]) + "\n")
            f.close()

            try:
                f = open("templates/analis/"+data[d][0].split("-")[0]+".html", "r")
            except:
                f = open("templates/analis/" + data[d][0].split("-")[0] + ".html", "w")
                f.write("{% extends 'analis/analis_index.html' %}\n{% block year %}\n\t<table>\n\t<tr><td>Data</td><td>Sozv/Grad</td><td>d/l</td><td>0 pr</td><td>Po vipad</td><td>Podryad</td><td>Luna b/k</td><td></td></tr></table>\t{% endblock %}")
                f.close()
                f = open("templates/analis/" + data[d][0].split("-")[0] + ".html", "r")


            text = f.read()
            f.close()

            count_0 = 0
            for i in form_string:
                if str(i) in text_2_1[-1]:
                    count_0 += 1

            list_of_thtow = []
            for i in range(len(form_string)):
                if int(text_2_1[-1][i]) in form_string:
                    list_of_thtow.append(str(i+1))


            list_of_thtow_sort = []
            for i in range(len(form_string)):
                if int(text_2_2[-1][i]) in form_string:
                    list_of_thtow_sort.append(str(i+1))

            new_string = "<tr><td>"+data[d][1]+"</td>"

            for i in range(2, 9):
                if i == 4:
                    new_string += "<td>"+str(count_0)+"</td>"
                elif i == 5:
                    new_string += "<td>"+" ".join(list_of_thtow)+"</td>"
                elif i == 6:
                    new_string += "<td>"+" ".join(list_of_thtow_sort)+"</td>"
                else:
                    new_string += "<td></td>"
            
            new_string += "</tr>"

            text_new = text.split("</table>")
            text_new[0]+=new_string
            join_text_new = "</table>".join(text_new)
            f = open("templates/analis/"+data[d][1].split("-")[0]+".html", "w")
            f.write(join_text_new)
            f.close()
            try:
                f = open("templates/statistic_keno/" + data[d][1].split("-")[0] + ".html", "r")
            except:
                f = open("templates/statistic_keno/" + data[d][1].split("-")[0] + ".html", "w")
                f.write(
                    "{% extends 'statistic_keno/statistic_index.html' %}\n{% block year %}\n\t<table>\n\t</table>\t{% endblock %}")
                f.close()
                f = open("templates/statistic_keno/" + data[d][1].split("-")[0] + ".html", "r")
            data_stat = f.read()
            f.close()
            data_stat = data_stat.split("</table>")

            row = ""
            row1 = ""
            row2 = ""
            row += "<tr>\n\t\t\t<td style = 'width: 250px'>" + data[d][1] + "</td>\n"

            for i in range(1, 81):
                if i in form_string:
                    if i % 10 == 1:
                        row += "\t\t\t<td style = 'background-color: pink; border-left: 3px solid black'></td>\n"
                    else:
                        row += "\t\t\t<td style = 'background-color: pink'></td>\n"
                else:
                    if i % 10 == 1:
                        row += "\t\t\t<td style = 'border-left: 3px solid black'></td>\n"
                    else:
                        row += "\t\t\t<td></td>\n"
            row += "\t\t</tr>\n"

            if data[d][1].split("-")[2] == "01" or data[d][1].split("-")[2] == "15":
                row1 += "<tr>\n\t\t\t<td style = 'width: 250px'></td>\n"
                row2 += "<tr>\n\t\t\t<td style = 'width: 250px'></td>\n"

                for i in range(0, 9):
                    for j in range(0, 10):
                        if (i == 0 and j == 0) or (i == 8 and j != 0):
                            continue
                        else:
                            if j % 10 == 1:
                                row1 += "\t\t\t<td style = 'background-color: green; border-left: 3px solid black'>" + str(
                                    i) + "</td>\n"
                                row2 += "\t\t\t<td style = 'background-color: green; border-left: 3px solid black'>" + str(
                                    j) + "</td>\n"
                            else:
                                row1 += "\t\t\t<td style = 'background-color: green'>" + str(i) + "</td>\n"
                                row2 += "\t\t\t<td style = 'background-color: green'>" + str(j) + "</td>\n"
                row1 += "\t\t</tr>\n"
                row2 += "\t\t</tr>\n"
                data_stat[0] = data_stat[0] + row1 + row2 + row + "\t\t</table>" + data_stat[1]
            else:
                data_stat[0] = data_stat[0] + row + "\t\t</table>" + data_stat[1]

            f = open("templates/statistic_keno/"+data[d][1].split("-")[0]+".html", "w")
            f.write(data_stat[0])
            f.close()

        return redirect(url_for('show', type = "keno", filename=data[d][0]))

    return render_template('keno_many.html')


@app.route("/maksima_one", methods=['GET', 'POST'])
def maksima_one():
    if request.method == 'POST':
        form_data = request.form

        form_string = form_data["numbers"].split(" ")[:-1]
        for i in range(len(form_string)):
            form_string[i] = int(form_string[i])

        f = open("data_maksima/" + str(int(form_data["number_game"]) - 1) + ".txt", "r")
        text = f.read()
        f.close()

        text = text.split("\n")
        for i in range(len(text)):
            text[i] = text[i].split(",")

        date = form_data["date"]

        text_2_1 = text[31:46]
        text_2_2 = text[46:61]

        text_2_1_c = deepcopy(text_2_1)
        text_2_2_c = deepcopy(text_2_2)

        text_2_1_n = delete_space(text_2_1_c, form_string)
        text_2_1_n.append(form_string)

        form_string_sort = deepcopy(form_string)
        form_string_sort.sort()
        text_2_2_n = delete_space(text_2_2_c, form_string_sort)
        text_2_2_n.append(form_string_sort)

        f = open("data_maksima/" + form_data["number_game"] + ".txt", "w")
        f.write(date + "\n")
        for i in [text_2_1, text_2_2, text_2_1_n, text_2_2_n]:
            for j in i:
                for k in range(len(j) - 1):
                    f.write(str(j[k]) + ",")
                f.write(str(j[-1]) + "\n")
        f.close()

        try:
            f = open("templates/statistic_maksima/" + form_data["date"].split("-")[0] + ".html", "r")
        except:
            f = open("templates/statistic_maksima/" + form_data["date"].split("-")[0] + ".html", "w")
            f.write(
                "{% extends 'statistic_maksima/statistic_index.html' %}\n{% block year %}\n\t<table>\n\t</table>\t{% endblock %}")
            f.close()
            f = open("templates/statistic_maksima/" + form_data["date"].split("-")[0] + ".html", "r")

        data = f.read()
        f.close()
        data = data.split("</table>")

        row = ""
        row1 = ""
        row2 = ""
        row += "<tr>\n\t\t\t<td style = 'width: 250px'>" + form_data["date"] + "</td>\n"

        for i in range(1, 46):
            if i in form_string:
                if i % 10 == 1:
                    row += "\t\t\t<td style = 'background-color: pink; border-left: 3px solid black'></td>\n"
                else:
                    row += "\t\t\t<td style = 'background-color: pink'></td>\n"
            else:
                if i % 10 == 1:
                    row += "\t\t\t<td style = 'border-left: 3px solid black'></td>\n"
                else:
                    row += "\t\t\t<td></td>\n"
        row += "\t\t</tr>\n"

        if form_data["date"].split("-")[2] == "01" or form_data["date"].split("-")[2] == "15":
            row1 += "<tr>\n\t\t\t<td style = 'width: 250px'></td>\n"
            row2 += "<tr>\n\t\t\t<td style = 'width: 250px'></td>\n"

            for i in range(0, 5):
                for j in range(0, 10):
                    if (i == 0 and j == 0) or (i == 4 and (j == 6 or j == 7 or j == 8 or j == 9)):
                        continue
                    else:
                        if j % 10 == 1:
                            row1 += "\t\t\t<td style = 'background-color: green; border-left: 3px solid black'>" + str(
                                i) + "</td>\n"
                            row2 += "\t\t\t<td style = 'background-color: green; border-left: 3px solid black'>" + str(
                                j) + "</td>\n"
                        else:
                            row1 += "\t\t\t<td style = 'background-color: green'>" + str(i) + "</td>\n"
                            row2 += "\t\t\t<td style = 'background-color: green'>" + str(j) + "</td>\n"
            row1 += "\t\t</tr>\n"
            row2 += "\t\t</tr>\n"
            data[0] = data[0] + row1 + row2 + row + "\t\t</table>" + data[1]
        else:
            data[0] = data[0] + row + "\t\t</table>" + data[1]

        f = open("templates/statistic_maksima/" + form_data["date"].split("-")[0] + ".html", "w")
        f.write(data[0])
        f.close()

        return redirect(url_for('show', type = "maksima", filename=form_data["number_game"]))

    return render_template('maksima_one.html')


@app.route("/maksima_many", methods=['GET', 'POST'])
def maksima_many():
    if request.method == 'POST':
        file = request.files["file_name"]
        filename = secure_filename(file.filename)
        file.save(os.path.join("sours_maksima/", filename))

        f = open("sours_maksima/" + filename)
        data = f.read()
        data = data.split("\n")[1:-2]
        for i in range(len(data)):
            data[i] = data[i].split("\t")[:2] + data[i].split("\t")[4:9]

        data.reverse()
        for d in range(len(data)):
            form_string = data[d][2:]
            for i in range(len(form_string)):
                form_string[i] = int(form_string[i])

            f = open("data_maksima/" + str(int(data[d][0]) - 1) + ".txt", "r")
            text = f.read()
            f.close()

            text = text.split("\n")
            for i in range(len(text)):
                text[i] = text[i].split(",")

            date = data[d][1]

            text_2_1 = text[31:46]
            text_2_2 = text[46:61]

            text_2_1_c = deepcopy(text_2_1)
            text_2_2_c = deepcopy(text_2_2)

            text_2_1_n = delete_space(text_2_1_c, form_string)
            text_2_1_n.append(form_string)

            form_string_sort = deepcopy(form_string)
            form_string_sort.sort()
            text_2_2_n = delete_space(text_2_2_c, form_string_sort)
            text_2_2_n.append(form_string_sort)

            f = open("data_maksima/" + data[d][0] + ".txt", "w")
            f.write(date + "\n")
            for i in [text_2_1, text_2_2, text_2_1_n, text_2_2_n]:
                for j in i:
                    for k in range(len(j) - 1):
                        f.write(str(j[k]) + ",")
                    f.write(str(j[-1]) + "\n")
            f.close()

            try:
                f = open("templates/statistic_maksima/" + data[d][1].split("-")[0] + ".html", "r")
            except:
                f = open("templates/statistic_maksima/" + data[d][1].split("-")[0] + ".html", "w")
                f.write(
                    "{% extends 'statistic_maksima/statistic_index.html' %}\n{% block year %}\n\t<table>\n\t</table>\t{% endblock %}")
                f.close()
                f = open("templates/statistic_maksima/" + data[d][1].split("-")[0] + ".html", "r")
            data_stat = f.read()
            f.close()
            data_stat = data_stat.split("</table>")

            row = ""
            row1 = ""
            row2 = ""
            row += "<tr>\n\t\t\t<td style = 'width: 250px'>" + data[d][1] + "</td>\n"

            for i in range(1, 46):
                if i in form_string:
                    if i % 10 == 1:
                        row += "\t\t\t<td style = 'background-color: pink; border-left: 3px solid black'></td>\n"
                    else:
                        row += "\t\t\t<td style = 'background-color: pink'></td>\n"
                else:
                    if i % 10 == 1:
                        row += "\t\t\t<td style = 'border-left: 3px solid black'></td>\n"
                    else:
                        row += "\t\t\t<td></td>\n"
            row += "\t\t</tr>\n"

            if data[d][1].split("-")[2] == "01" or data[d][1].split("-")[2] == "15":
                row1 += "<tr>\n\t\t\t<td style = 'width: 250px'></td>\n"
                row2 += "<tr>\n\t\t\t<td style = 'width: 250px'></td>\n"

                for i in range(0, 5):
                    for j in range(0, 10):
                        if (i == 0 and j == 0) or (i == 4 and (j == 6 or j == 7 or j == 8 or j == 9)):
                            continue
                        else:
                            if j % 10 == 1:
                                row1 += "\t\t\t<td style = 'background-color: green; border-left: 3px solid black'>" + str(
                                    i) + "</td>\n"
                                row2 += "\t\t\t<td style = 'background-color: green; border-left: 3px solid black'>" + str(
                                    j) + "</td>\n"
                            else:
                                row1 += "\t\t\t<td style = 'background-color: green'>" + str(i) + "</td>\n"
                                row2 += "\t\t\t<td style = 'background-color: green'>" + str(j) + "</td>\n"
                row1 += "\t\t</tr>\n"
                row2 += "\t\t</tr>\n"
                data_stat[0] = data_stat[0] + row1 + row2 + row + "\t\t</table>" + data_stat[1]
            else:
                data_stat[0] = data_stat[0] + row + "\t\t</table>" + data_stat[1]

            f = open("templates/statistic_maksima/" + data[d][1].split("-")[0] + ".html", "w")
            f.write(data_stat[0])
            f.close()

        return redirect(url_for('show', type="maksima", filename=data[d][0]))

    return render_template('maksima_many.html')


@app.route("/super_one", methods=['GET', 'POST'])
def super_one():
    if request.method == 'POST':
        form_data = request.form

        form_string = form_data["numbers"].split(" ")[:-1]
        for i in range(len(form_string)):
            form_string[i] = int(form_string[i])

        f = open("data_super/" + str(int(form_data["number_game"]) - 1) + ".txt", "r")
        text = f.read()
        f.close()

        text = text.split("\n")
        for i in range(len(text)):
            text[i] = text[i].split(",")

        date = form_data["date"]

        text_2_1 = text[31:46]
        text_2_2 = text[46:61]

        text_2_1_c = deepcopy(text_2_1)
        text_2_2_c = deepcopy(text_2_2)

        text_2_1_n = delete_space(text_2_1_c, form_string)
        text_2_1_n.append(form_string)

        form_string_sort = deepcopy(form_string)
        form_string_sort.sort()
        text_2_2_n = delete_space(text_2_2_c, form_string_sort)
        text_2_2_n.append(form_string_sort)

        f = open("data_super/" + form_data["number_game"] + ".txt", "w")
        f.write(date + "\n")
        for i in [text_2_1, text_2_2, text_2_1_n, text_2_2_n]:
            for j in i:
                for k in range(len(j) - 1):
                    f.write(str(j[k]) + ",")
                f.write(str(j[-1]) + "\n")
        f.close()

        try:
            f = open("templates/statistic_super/" + form_data["date"].split("-")[0] + ".html", "r")
        except:
            f = open("templates/statistic_super/" + form_data["date"].split("-")[0] + ".html", "w")
            f.write(
                "{% extends 'statistic_super/statistic_index.html' %}\n{% block year %}\n\t<table>\n\t</table>\t{% endblock %}")
            f.close()
            f = open("templates/statistic_super/" + form_data["date"].split("-")[0] + ".html", "r")

        data = f.read()
        f.close()
        data = data.split("</table>")

        row = ""
        row1 = ""
        row2 = ""
        row += "<tr>\n\t\t\t<td style = 'width: 250px'>" + form_data["date"] + "</td>\n"

        for i in range(1, 53):
            if i in form_string:
                if i % 10 == 1:
                    row += "\t\t\t<td style = 'background-color: pink; border-left: 3px solid black'></td>\n"
                else:
                    row += "\t\t\t<td style = 'background-color: pink'></td>\n"
            else:
                if i % 10 == 1:
                    row += "\t\t\t<td style = 'border-left: 3px solid black'></td>\n"
                else:
                    row += "\t\t\t<td></td>\n"
        row += "\t\t</tr>\n"

        if form_data["date"].split("-")[2] == "01" or form_data["date"].split("-")[2] == "15":
            row1 += "<tr>\n\t\t\t<td style = 'width: 250px'></td>\n"
            row2 += "<tr>\n\t\t\t<td style = 'width: 250px'></td>\n"

            for i in range(0, 6):
                for j in range(0, 10):
                    if (i == 0 and j == 0) or (i == 5 and j != 0 and j != 1  and j != 2):
                        continue
                    else:
                        if j % 10 == 1:
                            row1 += "\t\t\t<td style = 'background-color: green; border-left: 3px solid black'>" + str(
                                i) + "</td>\n"
                            row2 += "\t\t\t<td style = 'background-color: green; border-left: 3px solid black'>" + str(
                                j) + "</td>\n"
                        else:
                            row1 += "\t\t\t<td style = 'background-color: green'>" + str(i) + "</td>\n"
                            row2 += "\t\t\t<td style = 'background-color: green'>" + str(j) + "</td>\n"
            row1 += "\t\t</tr>\n"
            row2 += "\t\t</tr>\n"
            data[0] = data[0] + row1 + row2 + row + "\t\t</table>" + data[1]
        else:
            data[0] = data[0] + row + "\t\t</table>" + data[1]

        f = open("templates/statistic_super/" + form_data["date"].split("-")[0] + ".html", "w")
        f.write(data[0])
        f.close()

        return redirect(url_for('show', type="super", filename=form_data["number_game"]))

    return render_template('super_one.html')


@app.route("/super_many", methods=['GET', 'POST'])
def super_many():
    if request.method == 'POST':
        file = request.files["file_name"]
        filename = secure_filename(file.filename)
        file.save(os.path.join("sours_super/", filename))

        f = open("sours_super/" + filename)
        data = f.read()
        data = data.split("\n")[1:-2]
        for i in range(len(data)):
            data[i] = data[i].split("\t")[:2] + data[i].split("\t")[4:10]

        data.reverse()
        for d in range(len(data)):
            form_string = data[d][2:]
            for i in range(len(form_string)):
                form_string[i] = int(form_string[i])

            f = open("data_super/" + str(int(data[d][0]) - 1) + ".txt", "r")
            text = f.read()
            f.close()

            text = text.split("\n")
            for i in range(len(text)):
                text[i] = text[i].split(",")

            date = data[d][1]

            text_2_1 = text[31:46]
            text_2_2 = text[46:61]

            text_2_1_c = deepcopy(text_2_1)
            text_2_2_c = deepcopy(text_2_2)

            text_2_1_n = delete_space(text_2_1_c, form_string)
            text_2_1_n.append(form_string)

            form_string_sort = deepcopy(form_string)
            form_string_sort.sort()
            text_2_2_n = delete_space(text_2_2_c, form_string_sort)
            text_2_2_n.append(form_string_sort)

            f = open("data_super/" + data[d][0] + ".txt", "w")
            f.write(date + "\n")
            for i in [text_2_1, text_2_2, text_2_1_n, text_2_2_n]:
                for j in i:
                    for k in range(len(j) - 1):
                        f.write(str(j[k]) + ",")
                    f.write(str(j[-1]) + "\n")
            f.close()

            try:
                f = open("templates/statistic_super/" + data[d][1].split("-")[0] + ".html", "r")
            except:
                f = open("templates/statistic_super/" + data[d][1].split("-")[0] + ".html", "w")
                f.write(
                    "{% extends 'statistic_super/statistic_index.html' %}\n{% block year %}\n\t<table>\n\t</table>\t{% endblock %}")
                f.close()
                f = open("templates/statistic_super/" + data[d][1].split("-")[0] + ".html", "r")
            data_stat = f.read()
            f.close()
            data_stat = data_stat.split("</table>")

            row = ""
            row1 = ""
            row2 = ""
            row += "<tr>\n\t\t\t<td style = 'width: 250px'>" + data[d][1] + "</td>\n"

            for i in range(1, 53):
                if i in form_string:
                    if i % 10 == 1:
                        row += "\t\t\t<td style = 'background-color: pink; border-left: 3px solid black'></td>\n"
                    else:
                        row += "\t\t\t<td style = 'background-color: pink'></td>\n"
                else:
                    if i % 10 == 1:
                        row += "\t\t\t<td style = 'border-left: 3px solid black'></td>\n"
                    else:
                        row += "\t\t\t<td></td>\n"
            row += "\t\t</tr>\n"

            if data[d][1].split("-")[2] == "01" or data[d][1].split("-")[2] == "15":
                row1 += "<tr>\n\t\t\t<td style = 'width: 250px'></td>\n"
                row2 += "<tr>\n\t\t\t<td style = 'width: 250px'></td>\n"

                for i in range(0, 6):
                    for j in range(0, 10):
                        if (i == 0 and j == 0) or (i == 5 and j != 0 and j != 1  and j != 2):
                            continue
                        else:
                            if j % 10 == 1:
                                row1 += "\t\t\t<td style = 'background-color: green; border-left: 3px solid black'>" + str(
                                    i) + "</td>\n"
                                row2 += "\t\t\t<td style = 'background-color: green; border-left: 3px solid black'>" + str(
                                    j) + "</td>\n"
                            else:
                                row1 += "\t\t\t<td style = 'background-color: green'>" + str(i) + "</td>\n"
                                row2 += "\t\t\t<td style = 'background-color: green'>" + str(j) + "</td>\n"
                row1 += "\t\t</tr>\n"
                row2 += "\t\t</tr>\n"
                data_stat[0] = data_stat[0] + row1 + row2 + row + "\t\t</table>" + data_stat[1]
            else:
                data_stat[0] = data_stat[0] + row + "\t\t</table>" + data_stat[1]

            f = open("templates/statistic_super/" + data[d][1].split("-")[0] + ".html", "w")
            f.write(data_stat[0])
            f.close()

        return redirect(url_for('show', type="super", filename=data[d][0]))

    return render_template('super_many.html')


@app.route("/analis/<year>", methods=['GET', 'POST'])
@app.route("/analis", methods=['GET', 'POST'])
def analis(year = None):
    if year == "last":
        files = os.listdir("templates/analis")[:-1]
        full_list = [os.path.join("templates/analis", i) for i in files]
        time_sorted_list = max(full_list, key=os.path.getmtime)
        res = time_sorted_list.split("\\")
        res = res[1].split(".")[0]
    else:
        res = year
        
        
    return render_template("analis/"+res+".html", year = res)
    
    
@app.route("/d", methods=['GET', 'POST'])
def d():
    return render_template("analis/2020.html")


if __name__ == "__main__":
    app.debug = True
    app.run()