I = imread("/Users/olegsouzdalev/Desktop/Sem 7/CV/chelsea.png");

subplot(4,1,1);
I = rgb2gray(I);
imshow(I);
title('Original')

subplot(4,1,2);
Inew = imadjust(I);
imshow(Inew);
title('Imadjust')

subplot(4,1,3);
Inew = histeq(I);
imshow(Inew);
title('Histeq')

subplot(4,1,4);
Inew = adapthisteq(I);
imshow(Inew);
title('Adapthisteq')