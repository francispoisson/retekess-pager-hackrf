#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: Francis.Poisson
# GNU Radio version: 3.10.4.0

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from gnuradio import analog
from gnuradio import blocks
import pmt
from gnuradio import digital
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import osmosdr
import time
import random



from gnuradio import qtgui

class fsk_tx(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "fsk_tx")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.sps = sps = 2
        self.samp_rate_tx = samp_rate_tx = 8e6
        self.baud_rate = baud_rate = 10e3

        ##################################################
        # Blocks
        ##################################################
        
        self.generate_packet()
        
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=int(samp_rate_tx),
                decimation=(int(samp_rate_tx/baud_rate*sps*100)),
                taps=[],
                fractional_bw=0)
        self.osmosdr_sink_0 = osmosdr.sink(
            args="numchan=" + str(1) + " " + ""
        )
        self.osmosdr_sink_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.osmosdr_sink_0.set_sample_rate(samp_rate_tx)
        self.osmosdr_sink_0.set_center_freq(433.8e6, 0)
        self.osmosdr_sink_0.set_freq_corr(0, 0)
        self.osmosdr_sink_0.set_gain(50, 0)
        self.osmosdr_sink_0.set_if_gain(50, 0)
        self.osmosdr_sink_0.set_bb_gain(20, 0)
        self.osmosdr_sink_0.set_antenna('', 0)
        self.osmosdr_sink_0.set_bandwidth(0, 0)
        self.digital_gfsk_mod_0 = digital.gfsk_mod(
            samples_per_symbol=2,
            sensitivity=1.5,
            bt=1,
            verbose=False,
            log=False,
            do_unpack=True)
        self.blocks_multiply_xx_0_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff((-2))
        self.blocks_float_to_char_0 = blocks.float_to_char(1, 1)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, '/home/francis/Desktop/fsk/trame.dat', False, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_sink_1 = blocks.file_sink(gr.sizeof_gr_complex*1, '/home/francis/Desktop/fsk/generated_fsk_complex_8M', False)
        self.blocks_file_sink_1.set_unbuffered(False)
        self.blocks_char_to_float_0 = blocks.char_to_float(1, 1)
        self.blocks_add_const_vxx_0 = blocks.add_const_ff(1)
        self.analog_sig_source_x_0_0 = analog.sig_source_c(samp_rate_tx, analog.GR_COS_WAVE, 120e3, 1, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_multiply_xx_0_0, 1))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_float_to_char_0, 0))
        self.connect((self.blocks_char_to_float_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_char_to_float_0, 0))
        self.connect((self.blocks_float_to_char_0, 0), (self.digital_gfsk_mod_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.blocks_file_sink_1, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.osmosdr_sink_0, 0))
        self.connect((self.digital_gfsk_mod_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_multiply_xx_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "fsk_tx")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def bitfield(self, n):
        return [int(digit) for digit in bin(n)[2:]] # [2:] to chop off the "0b" part 

        
    def generate_packet(self):
        if((len(sys.argv)) < 2):
            raise Exception("Too few arguments")

        if not (sys.argv[1].startswith("0x")):
            raise Exception("call id must start with 0x and must be bcd-code (example: 301 = 0x301)")


        preamble = 0xaaaaaaaaaaaa1234a30c
        rolling_code = random.randint(0, 15)
        separator= 0x01
        cid = int(sys.argv[1][2:],16)

        print(rolling_code)

        nb_chiffre_significatif = 0

        if cid&0xF00 > 0:
            nb_chiffre_significatif += 1
        if cid&0x0F0 > 0:
            nb_chiffre_significatif += 1
        if cid&0x00F > 0:
            nb_chiffre_significatif += 1
    
        checksum1 = rolling_code+nb_chiffre_significatif-5
        if(checksum1 < 0):
            checksum1 = checksum1+16

        if (((cid&0xF00) >> 8) > (cid&0x00F)):
          checksum2 = ((cid&0xF00) >> 8)-1
        elif (((cid&0xF00) >> 8)==0) and (cid&0x00F == 0):
          checksum2 = 0xF
        elif ((cid&0x00F) > ((cid&0xF00)>>8)):
          checksum2 = (cid&0x00F)-1

        trame = int(preamble)<<72|int(rolling_code)<<68|int(separator)<<60|int(cid)<<48|int(checksum1)<<44|int(checksum2)<<40


        newFileBytes = self.bitfield(trame)
        newFileBytes.insert(0,0)

        trailing_zeroes = [b'0', b'0', b'0']

        data = newFileBytes+newFileBytes+newFileBytes+newFileBytes+newFileBytes+newFileBytes+newFileBytes+newFileBytes+newFileBytes+newFileBytes+trailing_zeroes

        data.insert(0,0)

        newdata = data[ : -31]

        newFile = open("trame.dat", "wb")
    
        newFileByteArray = bytearray(newdata)
        newFile.write(newFileByteArray)
        return

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps

    def get_samp_rate_tx(self):
        return self.samp_rate_tx

    def set_samp_rate_tx(self, samp_rate_tx):
        self.samp_rate_tx = samp_rate_tx
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate_tx)
        self.osmosdr_sink_0.set_sample_rate(self.samp_rate_tx)

    def get_baud_rate(self):
        return self.baud_rate

    def set_baud_rate(self, baud_rate):
        self.baud_rate = baud_rate




def main(top_block_cls=fsk_tx, options=None):


    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
