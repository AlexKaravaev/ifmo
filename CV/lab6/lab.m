I = imread('./input/circles.jpg');
t = graythresh(I);
blacked = im2bw(I, t);
blacked = ~blacked;
eroded  = bwmorph(blacked, 'erode', 65);
thickened = bwmorph(eroded, 'thicken', Inf);
res = ~(blacked & thickened);
imwrite(res, './res/circles_65.jpg');
