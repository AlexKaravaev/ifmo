I = imread("chelsea.png");

T = [1.1 0.35 0; 0.2 1.1 0; 0.00075 0.0005 1];
tform = projective2d(T);
I_projective = imwarp(I, tform);
%imshow(I_projective);

[numRows, numCols, Layers] = size(I); 
T = [0 0; 1 0; 0 1; 0.00001 0; 0.002 0; 0.001 0];
for k=1:1:Layers
    for y=1:1:numCols
        for x=1:1:numRows
            xnew = round(T(1,1)+T(2,1)*x+T(3,1)*y+T(4,1)*x^2+T(5,1)*x*y+T(6,1)*y^2);
            ynew = round(T(1,2)+T(2,2)*x+T(3,2)*y+T(4,2)*x^2+T(5,2)*x*y+T(6,2)*y^2); 
            I_polynomial(xnew,ynew,k) = I(x,y,k);
        end
    end
end
%imshow(I_polynomial);

[numRows, numCols, Layers] = size(I);
[xi,yi] = meshgrid(1:numCols,1:numRows);
imid = round(size(I,2)/2);
u = xi + 20*sin(2*pi*yi/90);
v = yi;
tmap_B = cat(3,u,v);
resamp = makeresampler('linear','fill');
I_sinusoid = tformarray(I,[],resamp,[2 1],[1 2],[],tmap_B,.3);
imshow(I_sinusoid);