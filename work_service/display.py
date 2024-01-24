

class Display:

    def __init__(self,  app, x, y):
        self.x = x
        self.y = y
        self.plot =app.plot.MPL

    def datamonitor(self):

        self.plot.cla()

        self.plot.title('离子步实时数据')
        self.plot.grid()

        self.plot.xlabel('迭代次数')
        self.plot.xlim(0,max(self.x)+1)
        self.plot.xticker(1.0,0.2)

        self.plot.ylabel('能量(eV)')
        self.plot.ylim(min(self.y)-1, max(self.y)+1)
        self.plot.yticker(1.0,0.2)

        self.plot.plot(self.x, self.y, '-or', linewidth=2.0, label='离子步')
        self.plot.legend(loc='upper right', shadow=True)

        self.plot.show()

        return


