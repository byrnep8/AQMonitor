#!/bin/bash
gatttool -b C5:47:25:9E:44:CE -t random --char-write-req --handle=0x0012 --value=0000
