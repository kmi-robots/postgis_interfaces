out = open('/home/gianluca/figures.html', 'w')

out.write('<!DOCTYPE html>')
out.write('<html>')
out.write('<head>')
out.write('<meta encoding="utf-8">')
out.write('<script src="http://www.x3dom.org/download/dev/x3dom.js"></script>')
out.write('<link rel="stylesheet" href="http://www.x3dom.org/download/dev/x3dom.css">')
out.write('</head>')

out.write('<body>')
out.write('<x3d xmlns="http://www.x3dom.org/x3dom" showStat="false" showLog="false"'
          ' x="0px" y="0px" width="1024px" height="768px">')
out.write('<scene>')
out.write('<viewpoint position=\'0 0 10\'></viewpoint>')


with open('/home/gianluca/xmldump.txt', 'r') as f:
    i = 0
    for line in f:
        solids = line.split(',')
        # for s in solids:
        out.write('<shape>')
        out.write('<appearance>')
        out.write('<material diffuseColor=\'0.603 0.894 0.909\' ></material>')
        out.write('</appearance>')
        # out.write(s)
        out.write(solids[1])
        out.write('</shape>')

out.write('<shape><plane></plane></shape>')
out.write('</scene>')
out.write('</x3d>')

out.write('</body>')
out.write('</html>')






