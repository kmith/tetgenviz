def export_to_xml(fname, vert_list, tet_list):

    f = open(fname, 'w')

    f.write('<?xml version="1.0"?>\n')
    f.write('<dolfin xmlns:dolfin="http://fenicsproject.org">\n')
    f.write('  <mesh celltype="tetrahedron" dim="3">\n')

    f.write('    <vertices size="%i">\n' % len(vert_list))
    for idx, v in enumerate(vert_list):
        f.write('      <vertex index="%i" x="%.8f" y="%.8f" z="%.8f" />\n' % (idx, v[0], v[1], v[2]))
    f.write('    </vertices>\n')

    f.write('    <cells size="%i">\n' % len(tet_list))
    for idx, t in enumerate(tet_list):
        f.write('      <tetrahedron index="%i" v0="%i" v1="%i" v2="%i" v3="%i" />\n' % (idx, t[0], t[1], t[2], t[3]))
    f.write('    </cells>\n')

    f.write('    <data />\n')
    f.write('  </mesh>\n')
    f.write('</dolfin>')

    f.close()
