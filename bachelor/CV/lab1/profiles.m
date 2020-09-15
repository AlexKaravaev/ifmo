I = imread("shape.png");
[numRows , numCols , Layers] = size(I);

% X axis
subplot(2,1,1);
x = [1 numCols];
y = [ceil(numRows/2) ceil(numRows/2)];
improfile(I,x,y);
grid on;

subplot(2,1,2);
x = [ceil(numCols/2) ceil(numCols/2)];
y = [1 numRows];
improfile(I,x,y);