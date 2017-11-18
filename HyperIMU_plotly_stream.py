'''
Created on 17 Nov 2017

@author: Johannes Friedrich
@mail: JohannesFriedrich@uni-bayreuth.de, 
@homepage GitHub: https://github.com/JohannesFriedrich 

'''

import plotly.plotly as py
from plotly.graph_objs import Stream, Scatter, Data, Layout, Figure
# auto sign-in with credentials or use py.sign_in()

from HIMUServer import HIMUServer

myHIMUServer = HIMUServer()

maxpoints = 200

stream1 = Stream(
    token='your_token_1',  # (!) link stream id to 'token' key
    maxpoints=maxpoints       
)

stream2 = Stream(
    token='your_token_2',  # (!) link stream id to 'token' key
    maxpoints=maxpoints       
)

stream3 = Stream(
    token='your_token_3',  # (!) link stream id to 'token' key
    maxpoints=maxpoints 
)


trace1 = Scatter(
        x=[],
        y=[], 
        mode='lines+markers',
        stream = stream1,
        name = 'Gyroscope z [rad/s]'
    )

trace2 = Scatter(
        x=[],
        y=[], 
        mode='lines+markers',
        stream = stream2,
        name = 'Accelerometer x [m/s^2]'
    )

trace3 = Scatter(
        x=[],
        y=[], 
        mode='lines+markers',
        stream = stream3,
        name = 'Rotation vector z'
    )


# combine traces to data
plotly_data = Data([trace1, trace2, trace3])


# Add title to layout object
layout = Layout(title='HyperIMU Real-time',
                yaxis=dict(
                    title='Unit'),
                xaxis = dict(
                    title = 'Data points'))

# Make a figure object
fig = Figure(data=plotly_data, layout=layout)

# (@) Send fig to Plotly, initialize streaming plot, open new tab
unique_url = py.plot(fig, filename='HyperIMU Real-Time plotter')


s1 = py.Stream('syypozzyhc')
s1.open()
s2 = py.Stream('zb4ptn0dir')
s2.open()
s3 = py.Stream('1cdyikdfvd')
s3.open()


import socket

HOST = ''              # Symbolic name meaning all available interfaces
PORT = 5557            # Arbitrary non-privileged port
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind((HOST, PORT))
socket.listen(1)
conn, addr = socket.accept()
conn.setblocking(1)
print 'Connected by', addr
i = 0
while 1:
    i += 1
    data = conn.recv(2048)
    data_split = data.split(",")
    if not data: break

    x = i
    y1 = data_split[3] # Gyroscope z
    y2 = data_split[4] # Accelerometer x
    y3 = data_split[9] # Rotationvector z
            
    # write x and y data to streams        
    s1.write(dict(x=x, y=y1))
    s2.write(dict(x=x, y=y2))
    s3.write(dict(x=x, y=y3))

conn.close()
print 'Connection closed'
s1.close()
s2.close()
s3.close()
