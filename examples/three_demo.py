
from py2js.decorator import JavaScript

def THREE():
  pass;

@JavaScript
def start_demo():  
  scene = _new(THREE.Scene);
  camera = _new(THREE.PerspectiveCamera, 75, window.innerWidth/window.innerHeight, 0.1, 1000);

  renderer = _new(THREE.WebGLRenderer);

  renderer.setSize(window.innerWidth, window.innerHeight);

  document.body.appendChild(renderer.domElement);

  geometry = _new(THREE.CubeGeometry, 1,1,1);
  material = _new(THREE.MeshBasicMaterial, js({color: 0x00ff00}));
  cube = _new(THREE.Mesh, geometry, material);

  scene.add(cube);

  setattr(camera.position, 'z', 5);

  @JavaScript
  def render(dt):
    requestAnimationFrame(render);
    cube.rotation.x += 0.1;
    cube.rotation.y += 0.1;
    renderer.render(scene, camera);

  render(0);
  
def main():
    print """<html>
<head>
<script language="JavaScript" src="../py-builtins.js"></script>
<script src="three.js"></script>
<script language="JavaScript">
%s
</script>
</head>
<body onLoad="start_demo()">
</body>
</html>""" % str(start_demo);

if __name__ == "__main__":
    main()
