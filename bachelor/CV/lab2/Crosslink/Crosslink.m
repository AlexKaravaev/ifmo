topPart = imread('chelsea_top.png');
botPart = imread('chelsea_bottom.png');
topPartHT = im2double(rgb2gray(topPart));
botPartHT = im2double(rgb2gray(botPart));

intersecPart = 5;
[numRows, numCols, Layers] = size(topPartHT);
[numRowsBot, numColsBot] = size(botPartHT);
botPartCorrHT = zeros(intersecPart,numCols);
topPartCorrHT = zeros(intersecPart,numCols);
correlationArray = [];

for j = 1:1:numCols
    for i = 1:1:intersecPart
        botPartCorrHT(i,j) = botPartHT(i,j);
    end
end

for j = 0:1:numRows-intersecPart
    for i = 1:1:intersecPart
        topPartCorrHT(i,:) = topPartHT(i+j,:);
    end
    correlationCoefficient = corr2(topPartCorrHT, botPartCorrHT);
    correlationArray = [correlationArray correlationCoefficient];
    correlationCoefficient = 0;
end
[M, I] = max(correlationArray);

numRowsBotCorr = numRowsBot + I - 1;
for k = 1:1:Layers
    for j = 1:1:numCols
        for i = 1:I-1
            result_img(i,j,k) = topPart(i,j,k);
        end
        for i = I:1:numRowsBotCorr
            result_img(i,j,k) = botPart(i-I+1,j,k);
        end
    end
end

imshow(result_img);
