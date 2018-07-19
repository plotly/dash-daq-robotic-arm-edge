from roboarm import Arm
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
from dash.dependencies import State, Input, Output

app = dash.Dash(__name__)

server = app.server
app.scripts.config.serve_locally = True


arm = Arm() 
vendor = 0x1267
bmRequestType = 0x40
bRequest = 6
wValue = 0x100
wIndex = 0

# CSS Imports
external_css = ["https://codepen.io/chriddyp/pen/bWLwgP.css",
                "https://cdn.rawgit.com/matthewchan15/dash-css-style-sheets/adf070fa/banner.css",
                "https://fonts.googleapis.com/css?family=Raleway:400,400i,700,700i",
                "https://fonts.googleapis.com/css?family=Product+Sans:400,400i,700,700i",
                "https://rawgit.com/matthewchan15/dash-sparki-icon-sheet/master/css/sparkibot.css"]


for css in external_css:
    app.css.append_css({"external_url": css})

app.layout = html.Div(
    [
        html.Div(
            id="container",
            style={"background-color": "#119DFF"},

            children=[
               html.H2(
                   "Dash DAQ: Robotic Arm Edge",
               ),
                html.A(
                   html.Img(
                       src="https://s3-us-west-1.amazonaws.com/plotly-tutorials/excel/dash-daq/dash-daq-logo-by-plotly-stripe+copy.png",
                   ),
                   href="http://www.dashdaq.io"
               )

            ],
            className="banner"
        ),
        html.Div(
            [
                html.Div(
                    id="dash-daq-remote-banner",
                    style={"position":"absolute",
                           "top":"138px",
                           "right":"-21px"},
                    children=[
                        html.A(
                            html.Img(
                                src="https://s3-us-west-1.amazonaws.com/plotly-tutorials/excel/dash-daq/dash-daq-logo-stripe.png",
                                style={"width":"50%"}
                            ),
                            href="http://www.dashdaq.io"
                        )
                    ]
                ),
                html.Div(
                    [
                        daq.Joystick(
                            id="LED-base-move",
                            force=0,
                            className="three columns", style={"paddingTop":"3%"}
                        ),
                        html.Div(
                            [
                                dcc.Textarea(
                                    id="serial-box",
                                    placeholder='Enter a value...',
                                    value='This is a TextArea component',
                                    style={'width': '98%',
                                           "height":"133px"}
                                ),
                                html.Div(
                                    [
                                        daq.Indicator(
                                            id="LED-state",
                                            label="LED ON/OFF",
                                            value=True,
                                            className="four columns",
                                            color="#EF553B",
                                            style={"textAlign":"center",
                                                   "marginLeft":"15%"}
                                        ),
                                        daq.Joystick(
                                            id="elbow-shoulder-move",
                                            force=0,
                                            className="six columns"
                                        )
                                    ], className="row", style={"marginTop":"5%"}
                                )
                            ], className="six columns"
                        ),
                        html.Div(
                            [
                                daq.Joystick(
                            id="wrist-grip-move",
                            force=0
                        ),
                            ], className="three columns", style={"paddingTop":"3%"}
                        )
                    ], className="row", style={ "width":"90%",
                                                "marginLeft":"1%",
                                                "paddingTop":"16%"}
                    ),
            ], style={"display": "flex",
                      "justify-content": "center",
                      "align-items": "center",
                      "border": "20px solid black",
                      "border-radius": "150px",
                      "height":"65%",
                      "width":"75%",
                      "marginLeft":"9%",
                      "marginRight":"9%",
                      "marginTop":"5.5%"}
        ),
        html.Div(
            [
                html.Div(id="wrist-grip-hold"),
                html.Div(id="elbow-shoulder-hold"),
                html.Div(id="LED-base-hold")

            ], style={"visibility": "hidden"}
        )
    ], style={'padding': '0px 10px 0px 10px',
              'marginLeft': 'auto',
              'marginRight': 'auto',
              "width": "693px",
              'height': "560px",
              'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)',
              "position": "absolute",
              "top": "0",
              "bottom": "0",
              "left": "0",
              "right": "0"}
)


# Wrist Grip move
@app.callback(
    Output("wrist-grip-hold", "children"),
    [Input("wrist-grip-move", "angle"),
     Input("wrist-grip-move", "force")]
)
def wrist_grip_move(angle, force):
    if force < 0.5: #STOP
        arm.wrist.stop()
        arm.grips.stop()
    elif angle < 135 and angle > 45: # UP 
        arm.wrist.up(None)
    elif angle < 315 and angle > 225: #DOWN
        arm.wrist.down(None)
    elif angle > 135 and angle < 225: #LEFT
        arm.grips.open(None)
    elif angle < 45 or angle > 345: #RIGHT
        arm.grips.close(None)
    return

# # Elbow Shoulder move
@app.callback(
    Output("elbow-shoulder-hold", "children"),
    [Input("elbow-shoulder-move", "angle"),
    Input("elbow-shoulder-move", "force")]
)
def elbow_shoulder_move(angle, force):
    if force < 0.5: #STOP
        arm.elbow.stop()
        arm.shoulder.stop()
    elif angle < 135 and angle > 45: # UP 
        arm.elbow.up(None)
    elif angle < 315 and angle > 225: #DOWN
        arm.elbow.down(None)
    elif angle > 135 and angle < 225: #LEFT
        arm.shoulder.up(None)
    elif angle < 45 or angle > 345: #RIGHT
        arm.shoulder.down(None)
    return

# # Base Led move
@app.callback(
    Output("LED-base-hold", "children"),
    [Input("LED-base-move", "angle"),
     Input("LED-base-move", "force")]
)
def elbow_shoulder_move(angle, force):
    if force < 0.5: #STOP
        arm.base.stop()
    elif angle < 135 and angle > 45: # UP 
        arm.led.on(None)
        led_color = "#00cc96"
    elif angle < 315 and angle > 225: #DOWN
        arm.led.off(None)
        led_color = "#EF553B"
    elif angle > 135 and angle < 225: #LEFT
        arm.base.rotate_counter(None)
    elif angle < 45 or angle > 345: #RIGHT
        arm.base.rotate_clock(None)
    return led_color

@app.callback(
    Output("LED-state", "color"),
    [Input("LED-base-hold","children")]
)
def LED_ON_OFF(LED_color):
    return LED_color

@app.callback(
    Output("serial-box", "value"),
    [Input("LED-base-move", "angle"),
    Input("LED-base-move", "force"),
    Input("elbow-shoulder-move", "angle"),
    Input("elbow-shoulder-move", "force"),
    Input("wrist-grip-move", "angle"),
    Input("wrist-grip-move", "force")]
)
def elbow_shoulder_move(LED_angle, LED_force, elbow_shoulder_angle, elbow_shoulder_force, wrist_grip_angle, wrist_grip_force):
    if elbow_shoulder_force < 0.5: #STOP
        command_one = "STOP"
    elif elbow_shoulder_angle < 135 and elbow_shoulder_angle > 45: # UP 
        command_one = "ELBOW UP"
    elif elbow_shoulder_angle < 315 and elbow_shoulder_angle > 225: #DOWN
        command_one = "ELBOW DOWN"
    elif elbow_shoulder_angle > 135 and elbow_shoulder_angle < 225: #LEFT
        command_one = "SHOULDER UP"
    elif elbow_shoulder_angle < 45 or elbow_shoulder_angle > 345: #RIGHT
        command_one = "SHOULDER DOWN"
    
    if LED_force < 0.5: #STOP
        command_two = "STOP"
    elif LED_angle < 135 and LED_angle > 45: # UP 
        command_two = "LED ON"
    elif LED_angle < 315 and LED_angle > 225: #DOWN
        command_two = "LED OFF"
    elif LED_angle > 135 and LED_angle < 225: #LEFT
        command_two = "BASE ROTATE LEFT"
    elif LED_angle < 45 or LED_angle > 345: #RIGHT
        command_two = "BASE ROTATE RIGHT"

    if wrist_grip_force < 0.5: #STOP
        command_three = "STOP"
    elif wrist_grip_angle < 135 and wrist_grip_angle > 45: # UP 
        command_three = "WRIST UP"
    elif wrist_grip_angle < 315 and wrist_grip_angle > 225: #DOWN
        command_three = "WRIST DOWN"
    elif wrist_grip_angle > 135 and wrist_grip_angle < 225: #LEFT
        command_three = "OPEN GRIP"
    elif wrist_grip_angle < 45 or wrist_grip_angle> 345: #RIGHT
        command_three = "CLOSE GRIP"
    
    text_monitor = ("-----CONTROL PANEL----\n\n" +
                    "Right Joystick: " +
                    command_one +
                    "\nLeft Joystick: " +
                    command_two +
                    "\nBottom Joystick: " +
                    command_three +
                    "\n\n" +
                    "---------READ ME---------\n" +
                    "This application was made to " +
                    "control the Robotic Arm Edge using " +
                    "the USB interface package. This" + 
                    " application can be controlled" +
                    " wirelessly using WIFI. See it " + 
                    "in action, by clicking " +
                    "on the Dash DAQ logo and reading the " +
                    "blog post titled, '"+
                    "Robotic Arm Edge'."
                    
                    )
    return text_monitor

if __name__ == '__main__':
    app.run_server(debug=True)

# Insert in app.run_server, to run through WI-FI: host="0.0.0.0" 
