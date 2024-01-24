import dash
from dash import dcc, html, Output, Input, State
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import requests


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.prevent_initial_callbacks = "initial_duplicate"

app.layout = html.Div(
    [
        dbc.Col(
            [ 
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Div(
                                [
                                    html.H2("Регистрация", className="text-center"),
                                    dbc.Form(
                                        [
                                         
                                            html.Div(
                                                [
                                                    dbc.Label("Username"),
                                                    dbc.Input(
                                                        type="text",
                                                        id="reg-username",
                                                    ),
                                                ],
                                                className="mb-3",
                                            ),
                                            html.Div(
                                                [
                                                    dbc.Label("Password"),
                                                    dbc.Input(
                                                        type="password",
                                                        id="reg-password",
                                                    ),
                                                ],
                                                className="mb-3",
                                            ),
                                            html.Div(
                                                [
                                                    dbc.Label("Кошелек"),
                                                    dbc.Input(
                                                        type="text",
                                                        id="reg-wallet",
                                                    ),
                                                ],
                                                className="mb-3",
                                            ),
                                            html.Div(
                                                [
                                                    dbc.Label("Возраст"),
                                                    dbc.Input(
                                                        type="text",
                                                        id="reg-name",
                                                    ),
                                                ],
                                                className="mb-3",
                                            ),
                                            dbc.Button(
                                                "Зарегистрироваться",
                                                id="btn-register",
                                                color="primary",
                                                className="mt-3",
                                            ),
                                            html.Div(
                                                id="output-register",
                                                className="text-center",
                                                style={"margin-top": "15px"},
                                            ),
                                        ],
                                    ),
                                ],
                                 style={"margin": "auto", "width": "auto"},
                             ),
                         ],
                         width={"size": 4, "offset": 0},
                     ),
                 ],
                 justify="center",
                 align="center",
                 className="mt-5",
             ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Div(
                                [
                                    html.H2("Авторизация", className="text-center"),
                                    dbc.Form(
                                        [
                                            html.Div(
                                                [
                                                    dbc.Label("Имя пользователя"),
                                                    dbc.Input(
                                                        type="text",
                                                        id="login-username",
                                                    ),
                                                ],
                                                className="mb-3",
                                            ),
                                            html.Div(
                                                [
                                                    dbc.Label("Пароль"),
                                                    dbc.Input(
                                                        type="password",
                                                        id="login-password",
                                                    ),
                                                ],
                                                className="mb-3",
                                            ),
                                            dbc.Button(
                                                "Войти",
                                                id="btn-login",
                                                color="primary",
                                                className="mt-3",
                                            ),
                                            html.Div(
                                                id="output-login",
                                                className="text-center",
                                                style={"margin-top": "15px"},
                                            ),
                                        ],
                                    ),
                                ],
                                style={"margin": "auto", "width": "auto"},
                            ),
                        ],
                        width={"size": 4, "offset": 0},
                    ),
                ],
                justify="center",
                align="center",
                className="mt-5",
            ),
            ],
            align="center",
            className="mt-5",
            id= "first-block-div"
        ),    
        html.Div(
            [
                html.Div(
                    [
                        html.H1("Баланс:"),
                        html.H1("Авторизация не пройдена", id="score-div"),
                        dcc.Interval(
                            id="interval-component",
                            interval=1300,  # in milliseconds
                            n_intervals=0,
                        ),
                        dcc.Store(id="token-store"),
                        html.H2("Выберите модель:"),
                    ],
                    style={"margin-left": "50px"}
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dcc.Dropdown(
                                    id="dropdown-model",
                                    options=[
                                        {
                                            "label": "Gboost 3 coins",
                                            "value": "gb",
                                        },
                                        {
                                            "label": "Rforest 2 points",
                                            "value": "rf",
                                        },
                                        {
                                            "label": "Lregression 1 points",
                                            "value": "lr",
                                        },
                                    ],
                                    value=None,
                                    style={"margin-left": "25px"},
                                ),
                            ],
                            width={"size": 3, "offset": 0},
                        ),
                    ],
                    justify="left",
                    align="left",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [   
                                html.Div(
                                    [
                                        html.H2(
                                            "Введите данные для прогноза выживаемости:"
                                        ),
                                    ],
                                    style={"margin-left": "50px",
                                           "margin-top": "20px"}
                                ),
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                html.Label("Количество дней болезни"),
                                                dcc.Slider(
                                                    id="slider-days",
                                                    min=0,
                                                    max=5000,
                                                    step=1,
                                                    value=None,
                                                    marks={
                                                        i: str(i)
                                                        for i in range(0, 5000, 250)
                                                    },
                                                ),
                                                html.Div(
                                                    id="slider-days-value"
                                                ),
                                            ],
                                            justify="center",
                                            align="center",
                                            style={"margin": "10px"},
                                        ),
                                        dbc.Row(
                                            [
                                                html.Label(
                                                    "Лечитесь ли вы препаратами?"
                                                ),
                                                dcc.Dropdown(
                                                    id="dropdown-drug",
                                                    options=[
                                                        {
                                                            "label": "Да",
                                                            "value": "1",
                                                        },
                                                        {
                                                            "label": "Нет",
                                                            "value": "0",
                                                        },
                                                    ],
                                                    value=None,
                                                ),
                                            ],
                                            className="mb-3",
                                            justify="center",
                                            align="center",
                                            style={"margin": "10px"},
                                        ),
                                        dbc.Row(
                                            [
                                             
                                                html.Label("Возраст"),
                                                dcc.Slider(
                                                    id="slider-age",
                                                    min=0,
                                                    max=100,
                                                    step=1,
                                                    value=None,
                                                    marks={
                                                        i: str(i)
                                                        for i in range(0, 100, 5)
                                                    },
                                                ),
                                                html.Div(
                                                    id="slider-age-value"
                                                ),
                                            ],
                                            justify="center",
                                            align="center",
                                            style={"margin": "10px"},
                                        ),
                                        dbc.Row(
                                            [
                                                html.Label(
                                                    "Пол"
                                                ),
                                                dcc.Dropdown(
                                                    id="dropdown-sex",
                                                    options=[
                                                        {
                                                            "label": "Мужчина",
                                                            "value": "1",
                                                        },
                                                        {
                                                            "label": "Женщина",
                                                            "value": "0",
                                                        },
                                                    ],
                                                    value=None,
                                                ),
                                            ],
                                            className="mb-3",
                                            justify="center",
                                            align="center",
                                            style={"margin": "10px"},
                                        ),
                                        dbc.Row(
                                            [
                                                html.Label(
                                                    "Асцит"
                                                ),
                                                dcc.Dropdown(
                                                    id="dropdown-asceties",
                                                    options=[
                                                        {
                                                            "label": "Есть",
                                                            "value": "1",
                                                        },
                                                        {
                                                            "label": "Нет",
                                                            "value": "0",
                                                        },
                                                    ],
                                                    value=None,
                                                ),
                                            ],
                                            className="mb-3",
                                            justify="center",
                                            align="center",
                                            style={"margin": "10px"},
                                        ),
                                        dbc.Row(
                                            [
                                                html.Label(
                                                    "Гепатомегалия"
                                                ),
                                                dcc.Dropdown(
                                                    id="dropdown-Hepatomegaly",
                                                    options=[
                                                        {
                                                            "label": "Есть",
                                                            "value": "1",
                                                        },
                                                        {
                                                            "label": "Нет",
                                                            "value": "0",
                                                        },
                                                    ],
                                                    value=None,
                                                ),
                                            ],
                                            className="mb-3",
                                            justify="center",
                                            align="center",
                                            style={"margin": "10px"},
                                        ),
                                        dbc.Row(
                                            [
                                                html.Label(
                                                    "Spiders"
                                                ),
                                                dcc.Dropdown(
                                                    id="dropdown-spiders",
                                                    options=[
                                                        {
                                                            "label": "Есть",
                                                            "value": "1",
                                                        },
                                                        {
                                                            "label": "Нет",
                                                            "value": "0",
                                                        },
                                                    ],
                                                    value=None,
                                                ),
                                            ],
                                            className="mb-3",
                                            justify="center",
                                            align="center",
                                            style={"margin": "10px"},
                                        ),
                                        dbc.Row(
                                            [
                                                html.Label(
                                                    "Эдема"
                                                ),
                                                dcc.Dropdown(
                                                    id="dropdown-edem",
                                                    options=[
                                                        {
                                                            "label": "Есть",
                                                            "value": "1",
                                                        },
                                                        {
                                                            "label": "Нет",
                                                            "value": "0",
                                                        },
                                                    ],
                                                    value=None,
                                                ),
                                            ],
                                            className="mb-3",
                                            justify="center",
                                            align="center",
                                            style={"margin": "10px"},
                                        ),
                                        dbc.Row(
                                            
                                            [
                                                html.Label("Билирубин"),
                                                dcc.Slider(
                                                    id="slider-bilirubin",
                                                    min=0,
                                                    max=30,
                                                    step=1,
                                                    value=None,
                                                    marks={
                                                        i: str(i)
                                                        for i in range(0, 30, 1)
                                                    },
                                                ),
                                                html.Div(
                                                    id="slider-bilirubin-value"
                                                ),
                                            ],
                                            justify="center",
                                            align="center",
                                            style={"margin": "10px"},
                                       
                                        ),
                                        dbc.Row(
                                            
                                            [
                                                html.Label("Холестерол"),
                                                dcc.Slider(
                                                    id="slider-cholesterol",
                                                    min=0,
                                                    max=400,
                                                    step=1,
                                                    value=None,
                                                    marks={
                                                        i: str(i)
                                                        for i in range(0, 400, 20)
                                                    },
                                                ),
                                                html.Div(
                                                    id="slider-cholesterol-value"
                                                ),
                                            ],
                                            justify="center",
                                            align="center",
                                            style={"margin": "10px"},
                                        
                                        ),
                                        dbc.Row(
                                            
                                            [
                                                html.Label("Альбумин"),
                                                dcc.Slider(
                                                    id="slider-albumin",
                                                    min=0,
                                                    max=10,
                                                    step=1,
                                                    value=None,
                                                    marks={
                                                        i: str(i)
                                                        for i in range(0, 10, 1)
                                                    },
                                                ),
                                                html.Div(
                                                    id="slider-albunim-value"
                                                ),
                                            ],
                                            justify="center",
                                            align="center",
                                            style={"margin": "10px"},
                                       
                                        ),
                                        dbc.Row(
                                            
                                            [
                                                html.Label("Copper"),
                                                dcc.Slider(
                                                    id="slider-copper",
                                                    min=0,
                                                    max=600,
                                                    step=1,
                                                    value=None,
                                                    marks={
                                                        i: str(i)
                                                        for i in range(0, 600, 50)
                                                    },
                                                ),
                                                html.Div(
                                                    id="slider-copper-value"
                                                ),
                                            ],
                                            justify="center",
                                            align="center",
                                            style={"margin": "10px"},
                                        
                                        ),
                                        dbc.Row(
                                            
                                            [
                                                html.Label("Alk_Phos"),
                                                dcc.Slider(
                                                    id="slider-alk",
                                                    min=0,
                                                    max=10000,
                                                    step=1,
                                                    value=None,
                                                    marks={
                                                        i: str(i)
                                                        for i in range(0, 10000, 500)
                                                    },
                                                ),
                                                html.Div(
                                                    id="slider-alk-value"
                                                ),
                                            ],
                                            justify="center",
                                            align="center",
                                            style={"margin": "10px"},
                                        
                                        ),
                                        dbc.Row(
                                            
                                            [
                                                html.Label("SGOT"),
                                                dcc.Slider(
                                                    id="slider-sgot",
                                                    min=0,
                                                    max=600,
                                                    step=1,
                                                    value=None,
                                                    marks={
                                                        i: str(i)
                                                        for i in range(0, 600, 50)
                                                    },
                                                ),
                                                html.Div(
                                                    id="slider-sgot-value"
                                                ),
                                            ],
                                            justify="center",
                                            align="center",
                                            style={"margin": "10px"},
                                       
                                        ),
                                        dbc.Row(
                                            [
                                                html.Label(
                                                    "Триглицериды"
                                                ),
                                                dcc.Slider(
                                                    id="slider-triglic",
                                                    min=0,
                                                    max=600,
                                                    step=1,
                                                    value=None,
                                                    marks={
                                                        i: str(i)
                                                        for i in range(
                                                            0, 600, 50
                                                        )
                                                    },
                                                ),
                                                html.Div(
                                                    id="slider-triglic-value"
                                                ),
                                            ],
                                            justify="center",
                                            align="center",
                                            style={"margin": "10px"},
                                        ),
                                    ],
                                ),
                                         dbc.Row(
                                            
                                            [
                                                html.Label("Platelets"),
                                                dcc.Slider(
                                                    id="slider-platelets",
                                                    min=0,
                                                    max=1000,
                                                    step=1,
                                                    value=None,
                                                    marks={
                                                        i: str(i)
                                                        for i in range(0, 1000, 1)
                                                    },
                                                ),
                                                html.Div(
                                                    id="slider-platelets-value"
                                                ),
                                            ],
                                            justify="center",
                                            align="center",
                                            style={"margin": "10px"},
                                        
                                        ),
                                dbc.Row(
                                            
                                            [
                                                html.Label("Протромбин"),
                                                dcc.Slider(
                                                    id="slider-protrombin",
                                                    min=0,
                                                    max=20,
                                                    step=1,
                                                    value=None,
                                                    marks={
                                                        i: str(i)
                                                        for i in range(0, 20, 1)
                                                    },
                                                ),
                                                html.Div(
                                                    id="slider-protrombin-value"
                                                ),
                                            ],
                                            justify="center",
                                            align="center",
                                            style={"margin": "10px"},
                                        
                                        ),
                                dbc.Row(
                                            
                                            [
                                                html.Label("Стадия болезни"),
                                                dcc.Slider(
                                                    id="slider-stage",
                                                    min=0,
                                                    max=4,
                                                    step=1,
                                                    value=None,
                                                    marks={
                                                        i: str(i)
                                                        for i in range(0, 4, 1)
                                                    },
                                                ),
                                                html.Div(
                                                    id="slider-stage-value"
                                                ),
                                            ],
                                            justify="center",
                                            align="center",
                                            style={"margin": "10px"},
                                        
                                        ),        
                                html.Div(
                                    [
                                        dbc.Button(
                                            "Получить данные",
                                            id="btn-get-data",
                                            style={"margin-right": "15px",
                                                   "margin-top": "20px"}
                                        ),
                                        dbc.Button(
                                            "Получить результат предсказания",
                                            id="btn-get-result",
                                            style={"margin-left": "15px",
                                                   "margin-top": "20px"}
                                        ),
                                    ],
                                    style={"margin-left": "50px"},
                                ),
                                html.Div(id="output-data",
                                         style={"margin-left": "50px",
                                                "margin-top": "20px"},),
                                html.Div(id="output-result",
                                         style={"margin-left": "50px",
                                                "margin-top": "20px"},),
                            ],
                        ),
                        dbc.Col(
                            [
                                html.Div(
                                    [
                                        html.H3("История результатов:"),
                                        html.Table(id="history-table"),
                                    ],
                                    style={"margin-top": "25px",
                                           "width": "auto",
                                           "margin-left": "50px",
                                           "margin-right": "50px"},
                                )
                            ]
                        ),
                    ],
                    justify="left",
                    align="left",
                ),
            ],
            id="second-block-div",
            style={"display": ""},
        ),
        dcc.Interval(
            id="interval-component-main",
            interval=1000,
            n_intervals=0,
        ),
    ],
    style={
        
        "background-color": "#ffffff",
    },
)

def get_results(url = "http://127.0.0.1:8000/user/get_res", token=None):
    headers = {"token": f"{token}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        history_strings = response.json()["res"]
        return history_strings, response.json()["res"]
    except:
        return []
    

def create_data_for_table(data):
    for x in range(len(data)):
        model = data[x]["model"]
        data_instance = (
            model,
            data[x]["result"],
        )
        data[x] = data_instance
    return reversed(data)

def create_res_form(raw_data, keys=(
        "Модель"),
):
    data = create_data_for_table(raw_data)
    table_rows = [
        html.Tr([html.Td(h) for h in row]) for row in data
    ]
    table = html.Table(
        [
            html.Thead(html.Tr([html.Th(k) for k in keys])),
            html.Tbody(table_rows),
        ]
    )

    return table
    


@app.callback(Output("output-register", "children"),[Input("btn-register", "n_clicks")],
    [
        State("reg-username", "value"),
        State("reg-password", "value"),
        State("reg-wallet", "value"),
        State("reg-age", "value"),
    ]
)
def register_callback(n_clicks, username, password, wallet, age):
    if n_clicks is None:
        raise PreventUpdate

    register_url = "http://127.0.0.1:8000/register"
    data = {
        "username": username,
        "password": password,
        "wallet": int(wallet),
        "age": int(age),
    }

    try:
        response = requests.post(register_url, json=data)
        response.raise_for_status()
        return response.json().get("message", "Registration successfull")
    except requests.HTTPError as e:
        return "Registration failed: Probably registred already"
    
@app.callback([Output("token-store", "data"),Output("history-table","children",allow_duplicate=True,),],
    [Input("btn-login", "n_clicks")],
    [
        State("login-username", "value"),
        State("login-password", "value"),
    ],
)
def login_callback(n_clicks, username, password):
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate

    login_url = "http://127.0.0.1:8000/token"
    data = {
        "username": username,
        "password": password,
    }

    try:
        response = requests.post(login_url, data=data)
        response.raise_for_status()
        access_token = response.json().get("access_token", "")
        hl, raw_data = get_results(token=access_token)
        return [access_token, create_res_form(raw_data)]
    except requests.HTTPError as e:
        return [None, html.Div("Не авторизован")]
    

@app.callback([Output(f"slider-{field}-value", "children")
               for field in ["Drug", "Age", "Sex"]],
              [
                Input(f"slider-{field}", "value")
                for field in ["Drug", "Age", "Sex"]])
def update_slider_values(drug, age, sex):
    return [
        f"Текущее значение: {value}"
        for value in [drug, age, sex]
    ]

@app.callback(
    Output("output-data", "children"),
    Input("btn-get-data", "n_clicks"),
    State("dropdown-model", "value"),
    State("slider-days", "value"),
    State("dropdown-drug", "value"),
    State("slider-age","value"),
    State("dropdown-sex", "value"),
    State("dropdown-asceties", "value"),
    State("dropdown-Hepatomegaly", "value"),
    State("dropdown-spiders", "value"),
    State("dropdown-edem", "value"),
    State("slider-bilirubin", "value"),
    State("slider-cholesterol", "value"),
    State("slider-albumin", "value"),
    State("slider-copper", "value"),
    State("slider-alk", "value"),
    State("slider-sgot", "value"),
    State("slider-platelets", "value"),
    State("slider-protrombin", "value"),
    State("slider-stage", "value"),
    
)
def get_and_display_data(n_clicks, model, days, drug, age, sex, asceties, Hepatomegaly, spiders, edem, bilirubin,                     
                          cholesterol, albumin, copper, alk, sgot, platelets, protrombin, stage):
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate

    data_str = f"Model: {model},Age: {age}, Drug: {drug}"

    return html.Div(data_str)


@app.callback(
    [
        Output(
            "history-table",
            "children",
            allow_duplicate=True,
        ),
    ],
    Input("btn-get-result", "n_clicks"),
    State("dropdown-model", "value"),
    State("slider-days", "value"),
    State("dropdown-drug", "value"),
    State("slider-age","value"),
    State("dropdown-sex", "value"),
    State("dropdown-asceties", "value"),
    State("dropdown-Hepatomegaly", "value"),
    State("dropdown-spiders", "value"),
    State("dropdown-edem", "value"),
    State("slider-bilirubin", "value"),
    State("slider-cholesterol", "value"),
    State("slider-albumin", "value"),
    State("slider-copper", "value"),
    State("slider-alk", "value"),
    State("slider-sgot", "value"),
    State("slider-triglic", "value"),
    State("slider-platelets", "value"),
    State("slider-protrombin", "value"),
    State("slider-stage", "value"),
    State("token-store","value")
)
def predict(n_clicks, model, days, drug, age, sex, asceties, Hepatomegaly, spiders, edem, bilirubin,                     
                          cholesterol, albumin, copper, alk, sgot, tryglyc, platelets, protrombin, stage, token):
    if n_clicks is not None:
        fast_api_inference_url = "http://127.0.0.1:8000/send_data"
        data = {
            "model_name": model,
            "N_Days":days,
             "Drug":drug,
             "Age":age,
             "Sex":sex,
             "Ascites":asceties,
             "Hepatomegaly":Hepatomegaly,
             "Spiders":spiders,
             "Edema":edem,
             "Bilirubin":bilirubin,
             "Cholesterol":cholesterol,
             "Albumin":albumin,
             "Copper":copper,
             "Alk_Phos":alk,
             "SGOT":sgot,
             "Triglycerides":tryglyc,
             "Platelets":platelets,
             "Prothrombin":protrombin,
             "Stage":stage,
             "token":token
        }
        try:
            response = requests.post(fast_api_inference_url, json=data)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return html.Div("Не авторизован")

        try:
            hl, raw_data = get_results(token=token)
            return [create_res_form(raw_data["model_name"])]
        except KeyError as e:
            return html.Div("Не авторизован")

@app.callback([Output("score-div", "children"),Output("first-block-div", "style"),
               Output("second-block-div", "style"),Output("history-table",
                                                          "children",
                                                          allow_duplicate=True)],
               [Input("interval-component-main", "n_intervals")],
               State("token-store", "data"))
def update_score(n, token):
    check_url = "http://127.0.0.1:8000/user/check"
    headers = {"Authorization": f"{token}"}
    try:
        response = requests.get(check_url, headers=headers)
        _, raw_data = get_results(token=token)
        response.raise_for_status() 
        return (
            response.json()["check"],
            {"display": "none"},
            {"display": ""},
            create_res_form(raw_data),
        )
    except:
        return "Not authorized", {"display": ""}, {"display": "none"}, None
    
if __name__ == "__main__":
    app.run_server(debug=False, host = '0.0.0.0')