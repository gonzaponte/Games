from ROOT import *

class Game:
    _colors         = [kBlack,kRed,kBlue,kOrange,kGreen,kPink+9,kViolet,kGray,kYellow,kMagenta]*100
    _filled_markers = [20,21,22,29,33,34]
    _empty_markers  = [24,25,26,30,27,28]

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
        tg.SetPoint(0,0,self.max_score)
        tg.SetPoint(1,self.max_score,self.max_score)
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
                scores, fix = self.ReadScores(input_str)
                if fix:
                    self.FixScore(scores)
                else:
                    self.AddHandScores(scores)

                if self.HasGameEnded():
                    self.EndGame()
                    self.NewGame()
            except:
                print 'Something went wrong. Try again...'

    def Finish( self ):
        self.logfile.close()

    def LoadPreviousSession( self ):

        print 'Loading previous session from %s...' % self.logfilename

        for line in open(self.logfilename,'r'):
            self.NewGame(False)
            for scorestr in line.split(' '):
                scores, fix = self.ReadScores(scorestr)
                self.AddHandScores(scores)
            self.EndGame(False)
        self.logfileopt = 'a'

        print 'DONE!'

    def NewGame( self, print_msg = True ):
        if print_msg:
            print '\n####### NEW GAME #######\n'
    
        self.BuildGraphs()
        self.scores = [0] * self.Nplayers
        self.lasts  = list(self.scores)
        self.hand   = 1
        self.game  += 1
        self.logstr = ''
    
    def EndGame( self, write = True ):
        for player,g in enumerate(self.graphs):
            g.SetLineStyle(2)
            g.SetMarkerStyle(self._empty_markers[player])
        if write:
            self.logfile.write(self.logstr[:-1] + '\n')

    def AddHandScores( self, scores ):
        for player, score in enumerate(scores):
            self.scores[player] += score
            if self.scores[player] < self.ylower:
                self.ylower = self.scores[player]
                self.MG.SetMinimum(self.ylower)
            if self.scores[player] > self.yupper:
                self.yupper = self.scores[player]
                self.MG.SetMaximum(self.yupper)
            self.graphs[player].SetPoint( self.hand, self.hand, self.scores[player] )
        
        print 'Current scores:', self.scores
        self.hand += 1
    
        if self.hand > self.xupper:
            self.xupper = self.hand
            self.MG.GetXaxis().SetLimits(self.xlower, self.xupper)
        
        self.canvas.Modified();self.canvas.Update()
        self.logstr += scores + ' '

    def FixScore( self, scores ):
        self.hand -= 1
        for player in range(self.Nplayers):
            self.scores[player] -= self.lasts[player]
        self.logstr = ' '.join(self.logstr.split(' ')[:-1]) + ' '
        self.AddHandScores( scores )

    def ReadScores( self, Istr ):
        scores = map( int, Istr.split(',') )
        return (scores[:-1], True) if len(scores) > self.Nplayers else (scores,False)
    
    def HasGameEnded( self ):
        return any(map( lambda x: x>self.max_score, self.scores ))

    def BuildGraph( self, player ):
        t = TGraph()
        t.SetMarkerStyle(self._filled_markers[player])
        t.SetLineColor  (self._colors [self.game])
        t.SetMarkerColor(self._colors [self.game])
        t.SetLineStyle  (1)
        t.SetPoint(0,0,0)
        return t

    def BuildGraphs( self ):
        self.graphs = map( self.BuildGraph, range(self.Nplayers) )
        map( self.MG.Add, self.graphs )



if __name__ == '__main__':
    Chinchon = Game(2,'chinchon.txt')









