I = imread("chelsea.png");

T = [1 0 0; 0.3 1 0; 0 0 1];
tform = affine2d(T);
I_bevel = imwarp(I, tform);
% imshow(I_bevel);

imid = round(size(I,2) / 2);
I_left = I(:, 1:imid, :);
stretch = 2;
I_right = I(:, (imid + 1:end), :);
T = [stretch 0 0; 0 1 0; 0 0 1];
tform = affine2d(T);
I_scale = imwarp(I_right, tform);
I_piecewiselinear = [I_left I_scale];
imshow(I_piecewiselinear);