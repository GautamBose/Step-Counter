import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.clock import Clock

from plyer import accelerometer

'''
This example uses Kivy Garden Graph addon to draw graphs plotting the
accelerometer values in X,Y and Z axes.
The package is installed in the directory: ./libs/garden/garden.graph
To read more about kivy garden, visit: http://kivy-garden.github.io/.
'''
from kivy.garden.graph import Graph, MeshLinePlot


class AccelerometerDemo(BoxLayout):
    def __init__(self):
        super(AccelerometerDemo, self).__init__()

        self.sensorEnabled = False
        self.graph = self.ids.graph_plot

        self.stepCount = 0
        self.zVals = []

        # For all X, Y and Z axes
        self.plot = []
        self.plot.append(MeshLinePlot(color=[1, 0, 0, 1]))  # X - Red
        self.plot.append(MeshLinePlot(color=[0, 1, 0, 1]))  # Y - Green
        self.plot.append(MeshLinePlot(color=[0, 0, 1, 1]))  # Z - Blue

        self.reset_plots()

        for plot in self.plot:
            self.graph.add_plot(plot)

    def reset_plots(self):
        for plot in self.plot:
            plot.points = [(0, 0)]

        self.counter = 1

    def do_toggle(self):
        try:
            if not self.sensorEnabled:
                accelerometer.enable()
                Clock.schedule_interval(self.get_acceleration, 5/1000)
                self.sensorEnabled = True
            else:
                accelerometer.disable()
                self.reset_plots()
                Clock.unschedule(self.get_acceleration)

                self.sensorEnabled = False
                
        except NotImplementedError:
                popup = ErrorPopup()
                popup.open()

    def get_acceleration(self, dt):
        if (self.counter == 100):
            # We re-write our points list if number of values exceed 100.
            # ie. Move each timestamp to the left.
            for plot in self.plot:
                del(plot.points[0])
                plot.points[:] = [(i[0] - 1, i[1]) for i in plot.points[:]]

            self.counter = 99

        val = accelerometer.acceleration[:3]

        if(not val == (None, None, None)):
            self.plot[0].points.append((self.counter, val[0]))
            self.plot[1].points.append((self.counter, val[1]))
            self.plot[2].points.append((self.counter, val[2]))
            self.zVals.append(val[2])
        
        if len(self.zVals) % 50 == 0 and len(self.zVals) >= 50:
            self.countSteps()
            self.ids.toggle_button.text = str(self.stepCount)
        elif len(self.zVals) < 50:
            self.ids.toggle_button.text = "initializing"


            #print(len(self.zVals))

        self.counter += 1
    
    def medianFiltering(self, zVals):
        filteredArray = []

        for i in range(len(zVals)):
            zVals[i] = zVals[i] - 9.8
            
            if i > 10:

                filteredArray.append(self.median(zVals[i-10 : i]))

        return filteredArray


    def deMeanValues(self, filteredArray):
        deMeanedArray = [None] * len(filteredArray)
        filteredArrayMean = sum(filteredArray) / len(filteredArray)

        for i in range(len(filteredArray)):
            deMeanedArray[i] = filteredArray[i] - filteredArrayMean

        return deMeanedArray


    def countZeros(self, deMeanedArray, filteredArray):
        i = 0
        zeroArray = [0] * len(deMeanedArray)

        while i < (len(filteredArray) - 30): 

            currentBuffer = deMeanedArray[i:i+30]

            # print(currentBuffer)

            for bufferIndex in range(len(currentBuffer) - 1):

                if currentBuffer[bufferIndex] < 0 and currentBuffer[bufferIndex+1] > 0:

                    zeroArray[bufferIndex + i] = 1

            i += 15
        return zeroArray

    #note this median function was copied off stackoverflow as there is no support
    # for the built in statistics module for the python interpreter for android
    def median(self, lst):
        sortedLst = sorted(lst)
        lstLen = len(lst)
        index = (lstLen - 1) // 2

        if (lstLen % 2):
            return sortedLst[index]
        else:
            return (sortedLst[index] + sortedLst[index + 1])/2.0

    def countSteps(self):

        zVals = self.zVals[-50:]
        filteredArray = self.medianFiltering(zVals)
        print(filteredArray)
        deMeanedArray = self.deMeanValues(filteredArray)
        zeroArray = self.countZeros(deMeanedArray, filteredArray)
        
        for i in range(len(zeroArray)):
            currentNumber = zeroArray[i]

            if currentNumber == 1:
                
                for val in deMeanedArray[i: i+20]:
                    if val > 0.3:
                        self.stepCount += 1
                        break


class AccelerometerDemoApp(App):
    def build(self):
        return AccelerometerDemo()

    def on_pause(self):
        return True


class ErrorPopup(Popup):
    pass


if __name__ == '__main__':
    AccelerometerDemoApp().run()
