

import sys, pupynere
ll = [l.strip().split(',') for l in open(sys.argv[1]) if not l.startswith('#')]
vv = zip(*[map(float, l) for l in ll])
nc = pupynere.netcdf_file(sys.argv[1]+'.nc', 'w')
nc.createDimension('dim', None)
for i in range(len(vv)):
    nc.createVariable('var_%02d' % i, 'd', ('dim',))[:] = vv[i]


