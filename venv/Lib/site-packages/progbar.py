#!/usr/bin/python
from __future__ import division
import sys
import os
import time
import threading
from math import floor

  
class ProgBar(threading.Thread):
    r"""
    A simple progression bar by Yves-Gwenael Bourhis
    
    Usage:
    ======
    
    Class ProgBar(name, lenght):
    ----------------------------
        name is a string
        lenght is an integer which represents the number of elements in the bar
        
    Methods:
    ========
    
    start():
    --------
        Start the progression bar in a thread
        the progression and thread stop automaticaly when the "percent" property reaches 100%
    
    stop():
    -------
        Stop the progression bar and the thread
        It is recommended to call the join() method after
    
    fill():
    -------
        Add an element to the bar, and match the corresponding percentage
 
    isAlive():
    ----------
        Returns True if the bar's thread is running, False otherwise
        
    join():
    -------
        Wait until the threaded bar terminates.
        It is recomended to call this method after a stop() call
        
    
    properties:
    ===========
    
    percent:
    --------
        percentage of the bar progression
        
    
    Example Using step progression::

        >>> def printatestbar1():
        ...     bar = ProgBar('test1', 20)
        ...     bar.start()
        ...     while bar.isAlive():
        ...         time.sleep(0.1)
        ...         bar.fill()
        ...     bar.join()
        >>> printatestbar1()
        test1 [####################] 100%
        >>> 
    
    Example Using percentage progression::

        >>> def printatestbar2():
        ...     bar = ProgBar('test2', 20)
        ...     bar.start()
        ...     while bar.isAlive():
        ...         bar.percent += 1
        ...         time.sleep(0.1)
        ...     bar.join()
        >>> printatestbar2()
        test2 [####################] 100%
        >>> 
    
    Example Interupting the progression bar::

        >>> def printatestbar3():
        ...     bar = ProgBar('test3', 20)
        ...     bar.start()
        ...     while bar.isAlive():
        ...         bar.percent += 1
        ...         if bar.percent == 50:
        ...             bar.stop()
        ...             break
        ...         time.sleep(0.1)
        ...     bar.join()
        >>> printatestbar3()
        test3 [##########-         ]  50%
        >>> 
    
    """
    
    def __init__(self, name= "Progression", lenght=60):
        self.len = lenght
        self.filled = 0
        self.blank = ' '
        self.fullchar = '#'
        self.begin = '['
        self.end = ']'
        self.progchars = ['|', '/','-', '\\']
        self.progchar = '>'
        self.prognum = len(self.progchars)
        self._percent = 0
        self.running = False
        threading.Thread.__init__(self, name=name)
        
    def __enter__():
        return self

    @property
    def progr(self):
        '''
        returns a different character from self.progchars each time it is called
        this makes the progression bar "look alive" while it's not progressing but running.
        '''
        if self.prognum < len(self.progchars):
            self.prognum += 1
        else:
            self.prognum = 1
        return self.progchars[self.prognum - 1]
    
    @property
    def percent(self):
        return self._percent
    
    @percent.setter
    def percent(self, prct):
        if isinstance(prct, int) and 0 <= prct <= 100:
            self._percent = prct
            self.filled = int( floor( (self._percent * (self.len/100) ) ))
        else:
            self._percent = int( floor( (self.filled / self.len) * 100) )
    
    @property    
    def bar(self):
        '''
        returns the string representing the progression bar
        '''
        _bar = self.begin
        _progr = ''.ljust(self.filled, self.fullchar)
        if self.filled < self.len:
            _progr = _progr.ljust(self.filled + 1, self.progr)
        _progr = _progr.ljust(self.len, self.blank)
        _bar += _progr
        _bar += self.end
        return _bar
    
    def fill(self):
        if self.filled < self.len:
            self.filled += 1
        self.percent = "more"
        
    def show(self):
        sys.stdout.write('\r{0:s} {1:s} {2:3d}%'.format(self.name, self.bar, self.percent))
        sys.stdout.flush()
        
    def run(self):
        self.running = self.isAlive()
        while self.percent < 100 and self.running:
            self.show()
            time.sleep(0.1)
        self.stop()
        self.show()
        sys.stdout.write('\n')
        
    def stop(self): 
        self.running = False
        
    def __exit__(self, exc_type=None, exc_value=None, traceback=None):
        self.stop()
        

def printatestbar1():
    bar = ProgBar(' test1', 20)
    bar.start()
    while bar.isAlive():
        time.sleep(0.1)
        bar.fill()
    bar.join()

def printatestbar2():
    bar = ProgBar(' test2', 20)
    bar.start()
    while bar.isAlive():
        bar.percent += 1
        time.sleep(0.1)
    bar.join()
    
def printatestbar3():
    bar = ProgBar(' test3', 20)
    bar.start()
    while bar.isAlive():
        bar.percent += 1
        if bar.percent == 50:
            bar.stop()
            break
        time.sleep(0.1)
    bar.join()

if __name__ == '__main__':
    printatestbar1()
    printatestbar2()
    printatestbar3()
    
