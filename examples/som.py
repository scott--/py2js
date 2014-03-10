from py2js.decorator import JavaScript

@JavaScript
def start_som():
  canvas = document.getElementById(js('canvas'));
  context = canvas.getContext("2d");
  
  # create an image
  image_data = context.createImageData(600, 600);
  
  # initialize data to noise
  for i in range(image_data.data.length):
    if i % 4 == 3:
      # leave alpha channel set to solid though
      image_data.data[i] = 255.0;
    else:
      image_data.data[i] = Math.random()*255;
    
  # write the image
  context.putImageData(image_data, 0, 0);
  
  # create the input data, 10 different colours
  samples = []; 
  samples.append((255, 0, 0)); # red
  samples.append((0, 255, 0)); # green
  samples.append((0, 0, 255)); # blue
  samples.append((200, 200, 200)); # light gray
  samples.append((100, 100, 100)); # dark gray
  samples.append((0, 0, 0)); # black
  samples.append((255, 255, 255)); # white
  samples.append((255, 255, 0)); # yellow
  samples.append((0, 255, 255)); # aqua
  samples.append((255, 0, 255)); # a fairly disgusting pink colour

  # a decreasing radius of influence that starts at 200
  radius = 400.0;
  
  # a decreasing learning rate that starts at 1
  learning_rate = 1.0;

  @JavaScript
  def update(dt):
    if radius > 0:
      # select one of the input samples at random
      sample = samples[Math.floor(Math.random() * len(samples))];
      
      # the current minimum dist
      min_dist = 100000000000000.0;
      #min_dist = Infinity;
      
      for i in range(0, image_data.data.length, 4):
        r = image_data.data[i];
        g = image_data.data[i+1];
        b = image_data.data[i+2];
        
        # get the euclidean distance between the sample and the
        # current data point
        dist = Math.sqrt((r - sample[0])*(r -  sample[0])+
          (g - sample[1])*(g - sample[1])+
          (b - sample[2])*(b-sample[2]));
          
        # if the sample is better than or equal to the best
        if dist <= min_dist:
          
          if dist < min_dist:
            # reset the list, there is only one best sample
            best_samples = [];
          
          # update the minimum distance
          min_dist = dist;
          
          # get the location (x, y)
          x = Math.floor(i/4) % (image_data.width);
          y = Math.floor(i / (image_data.width*4));
          best_sample = (x, y)

          # add the sample
          best_samples.append(best_sample);

            
      # choose one of the best samples at random
      best_sample = best_samples[Math.floor(Math.random() * len(best_samples))];
      bx = best_sample[0];
      by = best_sample[1];
            
      for i in range(0, image_data.data.length, 4):
        r = image_data.data[i];
        g = image_data.data[i+1];
        b = image_data.data[i+2];
        
        x = Math.floor(i/4) % (image_data.width);
        y = Math.floor(i / (image_data.width * 4));
        
        # get the euclidean distance from the best sample 
        # by location this time
        dist = Math.sqrt((x - bx)*(x-bx) + (y - by)*(y - by));
        
        if dist < radius:
          # set t to be a value between 0 and 1 representing how close
          # a neighbour is to the best sample
          t = (radius - dist)/radius*learning_rate;
          image_data.data[i] = (1. - t) * r + t * sample[0];
          image_data.data[i+1] = (1. - t) * g + t * sample[1];
          image_data.data[i+2] = (1. - t) * b + t * sample[2];

      
      # reduce the radius of influence and learning rate.
      radius -= 0.2;
      learning_rate -= 0.0005;
      
      context.putImageData(image_data, 0, 0);
    
    window.requestAnimationFrame(update);

  window.requestAnimationFrame(update);

def main():
    print """<html>
<head>
<script language="JavaScript" src="../py-builtins.js"></script>
<script language="JavaScript">
%s
</script>
</head>
<body onload="%s">
  <canvas id="canvas" width="1024" height="768"></canvas>
</body>
</html>""" % (str(start_som), "start_som();");


if __name__ == "__main__":
    main()
