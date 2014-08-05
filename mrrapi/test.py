# -*- coding: utf-8 -*-
import mrrapi

demo = mrrapi.api('key','secret')

print "Rig Detail 6899"
print demo.rig_detail(6899)
print "List Scrypt rigs over 10 MH"
print demo.rig_list(10,0,0,0)
print "List X11 rigs"
print demo.rig_list(0,0,0,0,'x11')
