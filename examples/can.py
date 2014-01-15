from py2js.decorator import JavaScript

@JavaScript
def start_can():
  class Cell(object):
    def __init__(self, x, y):
      self.x = x;
      self.y = y;
      self.energy = 0;

    def dist_betw(self, x, y):
      return Math.sqrt((self.x - x)*(self.x - x) + (self.y - y)*(self.y - y));

    def __str__(self):
      return "%f %f %f" % (self.x, self.y, self.energy);

  class CAN(object):
    def __init__(self, num_cells):
      self.cells = [];
      for i in range(num_cells):
        self.cells.append(Cell(Math.random(), Math.random()));

    def inject(self, x, y, energy, radius):
      total_weight = 0.;
      for cell in self.cells:
        dist_betw = cell.dist_betw(x, y);
        if dist_betw < radius:
          total_weight += (radius - dist_betw)/radius;
        
      normalizer = 1./total_weight;
        
      for cell in self.cells:
        dist_betw = cell.dist_betw(x, y);
        if dist_betw < radius:
          cell.energy += (radius - dist_betw)/radius*normalizer*energy;

    def excite(self, radius):
      for cell1 in self.cells:
        cell1.new_energy = 0;

      for cell1 in self.cells:
        if cell1.energy < 0.01:
          cell1.energy = 0;
          continue;
        total_weight = 0;
        cells_to_change = [];
        for cell2 in self.cells:
          dist_betw = cell1.dist_betw(cell2.x, cell2.y);
          if dist_betw < radius:
            total_weight += (radius - dist_betw)/radius;
            cells_to_change.append(cell2);
            cell2.new_energy += (radius - dist_betw)/radius*cell1.energy;

        normalizer = 1./total_weight;      
        for cell2 in cells_to_change:
          cell2.new_energy += cell2.new_energy * normalizer;

      for cell1 in self.cells:
        cell1.energy = cell1.new_energy;
            
    def inhibit(self, radius):
      for cell1 in self.cells:
        cell1.new_energy = 0;

      for cell1 in self.cells:
        if cell1.energy < 0.01:
          cell1.energy = 0;
          continue;
        total_weight = 0;
        cells_to_change = [];
        for cell2 in self.cells:
          dist_betw = cell1.dist_betw(cell2.x, cell2.y);
          if dist_betw < radius:
            total_weight += (radius - dist_betw)/radius;
            cells_to_change.append(cell2);
            cell2.new_energy += (radius - dist_betw)/radius*cell1.energy;

        normalizer = 1./total_weight;      
        for cell2 in cells_to_change:
          cell2.new_energy += cell2.new_energy * normalizer;

      for cell1 in self.cells:
        cell1.energy -= cell1.new_energy;


    def normalize(self):
      total_energy = 0;
      for cell in self.cells:
        total_energy += cell.energy;

      for cell in self.cells:
        cell.energy /= total_energy;
        
    def move(self, dx, dy):
      for cell1 in self.cells:
        cell1.new_energy = 0;
      for cell1 in self.cells:
        if cell1.energy < 0.01:
          continue;
        x = cell1.x + dx;
        y = cell1.y + dy;
        min_cell = None;
        min_dist_betw = 1.0;
        for cell2 in self.cells:
          dist_betw = cell2.dist_betw(x, y);
          if dist_betw < min_dist_betw:
            min_dist_betw = dist_betw;
            min_cell = cell2;
        
        min_cell.new_energy += cell1.energy;
      
      for cell1 in self.cells:
        cell1.energy = cell1.new_energy;

    def draw(self):
      ctx = document.getElementById(js('canvas')).getContext(js('2d'));
      
      for cell in self.cells:
        ctx.beginPath();
        setattr(ctx, "fillStyle", "rgb(%f, %f, %f)" % 
          (Math.floor(255-cell.energy*100*255), 
          Math.floor(255-cell.energy*100*255), 
          Math.floor(255-cell.energy*100*255)));
        ctx.moveTo(cell.x*768+10,cell.y*768);
        ctx.arc(cell.x*768,cell.y*768,10,0,Math.PI*2,true);
        ctx.closePath();
        ctx.fill();
        ctx.stroke();

    def __str__(self):
      s = "";    
      for cell in self.cells:
        s += cell.__str__() + "\n";
      return s;

  mouse_down = False;
  mouse_x = 0;
  mouse_y = 0;
  
  key_left = False;
  key_right = False;
  key_up = False;
  key_down = False;

  @JavaScript
  def on_mouse_down(e):
    global mouse_down;
    mouse_down = True;

  @JavaScript
  def on_mouse_up(e):
    global mouse_down;
    mouse_down = False;

  @JavaScript
  def on_mouse_move(e):
    global mouse_x, mouse_y;
    mouse_x = e.pageX - e.target.offsetLeft;
    mouse_y = e.pageY - e.target.offsetTop;
    
  @JavaScript
  def on_key_down(e):
    global key_left, key_right, key_up, key_down;
    if event.keyCode == 37: #left
      key_left = True;
    elif event.keyCode == 39: # right
      key_right = True;
    elif event.keyCode == 38: # up
      key_up = True;
    elif event.keyCode == 40: # down
      key_down = True;

  @JavaScript
  def on_key_up(e):
    global key_left, key_right, key_up, key_down;
    if event.keyCode == 37: #left
      key_left = False;
    elif event.keyCode == 39: # right
      key_right = False;
    elif event.keyCode == 38: # up
      key_up = False;
    elif event.keyCode == 40: # down
      key_down = False;
  
  can = CAN(1000);
  can.inject(0.5, 0.5, 1, 0.2);
  can.normalize();

  canvas = document.getElementById(js('canvas'));
  canvas.addEventListener("mousedown", on_mouse_down);
  canvas.addEventListener("mouseup", on_mouse_up);
  canvas.addEventListener("mousemove", on_mouse_move);
  canvas.addEventListener("keydown", on_key_down);
  canvas.addEventListener("keyup", on_key_up);
  canvas.setAttribute("tabindex", "0");


  @JavaScript
  def update(dt):
    global mouse_x, mouse_y, mouse_down;
    if mouse_down:
      can.inject(mouse_x/768, mouse_y/768, 0.5, 0.2);
    
    vx = 0.;
    vy = 0.;
    if key_up:
      vy = -0.05;
    elif key_down:
      vy = 0.05;
    
    if key_left:
      vx = -0.05;
    elif key_right:
      vx = 0.05;
    
    if Math.abs(vx) > 0.01 or Math.abs(vy) > 0.01:
      can.move(vx, vy);
    
    can.excite(0.2);
    can.inhibit(0.16);
    can.normalize();
    can.draw();
    window.requestAnimationFrame(update);

  window.requestAnimationFrame(update);

def main():
    print """<html>
<head>
<!--[if IE]><script type="text/javascript" src="http://explorercanvas.googlecode.com/svn/trunk/excanvas.js"></script><![endif]-->
<script language="JavaScript" src="../py-builtins.js"></script>
<script language="JavaScript">
%s
</script>
</head>
<body onLoad="start_can()">
  <canvas id="canvas" width="1024" height="768"></canvas>
</body>
</html>""" % str(start_can);


if __name__ == "__main__":
    main()
