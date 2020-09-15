I = imread("barcode.png");
I = imbinarize(I);
I = not(I);
[numRows , numCols , Layers] = size(I);

for i=1:1:numRows
Proj(i,1) = sum(I(i,:)) / 256;
end

subplot(2,1,1);
plot(Proj, (1:1:numRows));
title('Projection on Y');

for i=1:1:numCols
Proj(i,1) = sum(I(:,i)) / 256;
end

subplot(2,1,2);
plot((1:1:numCols), Proj);
title('Projection on X');