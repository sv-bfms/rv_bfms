'''
Created on Oct 6, 2019

@author: ballance
'''

import cocotb
from cocotb.drivers import Driver
from cocotb.triggers import RisingEdge, ReadOnly, Lock, Event


@cocotb.bfm(hdl={
    cocotb.bfm_vlog : cocotb.bfm_hdl_path(__file__, "hdl/rv_data_out_bfm.v"),
    cocotb.bfm_sv   : cocotb.bfm_hdl_path(__file__, "hdl/rv_data_out_bfm.v")
    })
class ReadyValidDataOutBFM():

    def __init__(self):
        self.busy = Lock()
        self.ack_ev = Event()

    @cocotb.coroutine
    def write_c(self, data):
        '''
        Writes the specified data word to the interface
        '''
        
        yield self.busy.acquire()
        self._write_req(data)

        # Wait for acknowledge of the transfer
        yield self.ack_ev.wait()
        self.ack_ev.clear()

        self.busy.release()

    @cocotb.bfm_import(cocotb.bfm_uint32_t)
    def _write_req(self, d):
        pass
    
    @cocotb.bfm_export()
    def _write_ack(self):
        self.ack_ev.set()
    
