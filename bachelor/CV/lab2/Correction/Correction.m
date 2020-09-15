I = imread("chelsea.png");

%Barrel Distortion
[numRows, numCols, Layers] = size(I);
[xi,yi] = meshgrid(1:numCols,1:numRows);
imid = round(size(I,2)/2);
xt = xi(:) - imid;
yt = yi(:) - imid;

[theta,r] = cart2pol(xt,yt);
%COEFFICIENTS
F3 = .0000001;
F5 = .0000001;
R = r + F3 * r.^2 + F5 * r.^4;

[ut,vt] = pol2cart(theta, R);
u = reshape(ut, size(xi)) + imid;
v = reshape(vt, size(yi)) + imid;
tmap_B = cat(3, u, v);
resamp = makeresampler('linear','fill');
I_barrel = tformarray(I,[],resamp,[2 1],[1 2],[],tmap_B,.3);
%imshow(I_barrel);

% CORRECTION BY INVERSE CUSHION DISTORTION
[numRows, numCols, Layers] = size(I_barrel);
[xi,yi] = meshgrid(1:numCols,1:numRows);
imid = round(size(I_barrel,2)/2);
xt = xi(:) - imid;
yt = yi(:) - imid;

[theta,r] = cart2pol(xt,yt);
%COEFFICIENTS
F3 = -.0000001;
R_2 = r + F3 * r.^2;

[ut,vt] = pol2cart(theta, R_2);
u = reshape(ut, size(xi)) + imid;
v = reshape(vt, size(yi)) + imid;
tmap_B = cat(3, u, v);
resamp = makeresampler('linear','fill');
I_barrel_2 = tformarray(I,[],resamp,[2 1],[1 2],[],tmap_B,.3);
imshow(I_barrel_2);