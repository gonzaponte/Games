from ROOT import *

class Game:
    _colors  = [kBlack,kRed,kBlue,kOrange,kGreen,kPink+9,kViolet,kGray,kYellow,kMagenta]*100
    _markers = range(20,25)

    def __init__( self, Nplayers, logfilename = 'chinchon.txt', max_score = 100 ):
        self.logfilename = logfilename
        self.Nplayers    = Nplayers
        self.max_score   = max_score
        self.logfileopt  = 'w'
        
        # Graphics variables
        self.xlower = 0.0
        self.xupper = 1.0
        self.ylower = 0.0
        self.yupper = 150
        self.canvas = TCanvas()
        self.MG     = TMultiGraph()
        self._CreateDeadline()
        
        # Game variables
        self.game   = 0
        self.hand   = 0
        self.scores = [0] * self.Nplayers
        self.logstr = ''
    
        self.Start()
        self.Finish()

    def _CreateDeadline( self ):
        
        tg = TGraph()
        tg.SetMarkerStyle(0)
        tg.SetLineColor(kRed)
        tg.SetLineWidth(3)
        tg.SetPoint(0,0,max_score)
        tg.SetPoint(1,max_score,max_score)
        self.MG.Add(tg)
        self.MG.Draw('APL')
        self.MG.GetXaxis().SetTitle('Hand')
        self.MG.GetYaxis().SetTitle('Score')
        self.MG.GetXaxis().SetLimits(self.xlower, self.xupper)
        self.MG.SetMinimum(self.ylower);self.MG.SetMaximum(self.yupper)
        self.canvas.Modified();self.canvas.Update()
    
    def Start( self ):
        if 'y' in raw_input('Load previous session (y/n)? '):
            self.LoadPreviousSession()
        
        self.logfile = open( self.logfilename, self.logfileopt )
        self.NewGame()
        
        while True:
            input_str = raw_input('Introduce hand scores: ')
            if input_str == 'exit': break
            try:
                self.AddHandScores(input_str)

                if self.HasGameEnded():
                    self.EndGame()
                    self.NewGame()
            except:
                print 'Something went wrong. Try again...'

    def Finish( self ):
        self.logfile.close()

    def LoadPreviousSession():

        print 'Loading previous session from %s...' % logfile

        for line in open(self.logfilename,'r'):
            self.NewGame(False)
            for scores in line.split(' '):
                self.AddHandScores(scores)
            self.EndGame(False)
        self.logfileopt = 'a'

        print 'DONE!'

    def NewGame( self, print_msg = True ):
        if print_msg:
            print '\n####### NEW GAME #######\n'
    
        self.BuildGraphs()
        self.scores = [0] * self.Nplayers
        self.hand   = 0
        self.game  += 1
        self.logstr = ''
    
    def EndGame( self, write = True ):
        for g in self.graphs:
            g.SetLineStyle(2)
            g.SetMarkerSize(0.5)
        if write:
            self.logfile.write(self.logstr[:-1] + '\n')

    def AddHandScores( self, scores ):
        for player, score in enumerate(self.ReadScores(scores)):
            self.scores[player] += score
            if self.scores[player] < self.ylower:
                self.ylower = self.scores[player]
                self.MG.SetMinimum(self.ylower)
            if self.scores[player] > self.yupper:
                self.yupper = self.scores[player]
                self.MG.SetMaximum(self.yupper)
            self.graphs[player].SetPoint( self.hand, self.hand, self.scores[player] )

        self.hand += 1
    
        if self.hand > self.xupper:
            self.xupper = self.hand
            self.MG.GetXaxis().SetLimits(self.xlower, self.xupper)
        
        self.canvas.Modified();self.canvas.Update()
        self.logstr += scores + ' '

    def ReadScores( self, Istr ):
        return map( int, Istr.split(',') )
    
    def HasGameEnded( self ):
        return any(map( lambda x: x>self.max_score, self.scores ))

    def BuildGraph( self, player ):
        t = TGraph()
        t.SetMarkerStyle(self._markers[player])
        t.SetLineColor  (self._colors [self.game])
        t.SetMarkerColor(self._colors [self.game])
        t.SetLineStyle  (1)
        return t

    def BuildGraphs( self ):
        self.graphs = map( self.BuildGraph, range(self.Nplayers) )
        map( self.MG.Add, self.graphs )



if __name__ == '__main__':
    Chinchon = Game(2,'chinchon.txt')









