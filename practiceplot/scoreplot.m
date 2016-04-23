
%% Initialization
clear ; close all; clc

%% Load Data

data = csvread('scores.csv');
X = data(:,[1]); y = data(:,[2]);

scatter(X, y);

% Put some labels 
hold on;
% Labels and Legend
xlabel('Win Score')
ylabel('Lose Score')



