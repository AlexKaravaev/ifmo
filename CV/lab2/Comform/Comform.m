
I = imread("chelsea.png");

T = [1 0 0; 0 1 0; 50 100 1];
tform = affine2d(T);
I_shift = imwarp(I, tform, 'Interp', 'nearest', 'OutputView', imref2d(size(I), [1 size(I,2)], [1 size(I,1)]));
%imshow(I_shift);

T = [1 0 0; 0 -1 0; 0 0 1];
tform = affine2d(T);
I_reflect = imwarp(I, tform);
%imshow(I_reflect);

T = [2 0 0; 0 2 0; 0 0 1];
tform = affine2d(T);
I_scale = imwarp(I, tform);
%imshow(I_scale);

phi = 17*pi/180;
T = [cos(phi) sin(phi) 0; -sin(phi) cos(phi) 0; 0 0 1];
tform = affine2d(T);
I_rotate = imwarp(I, tform);
imshow(I_rotate);
