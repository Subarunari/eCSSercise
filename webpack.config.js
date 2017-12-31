"use strict";
const path = require("path");
const webpack = require("webpack");
const ExtractTextPlugin = require('extract-text-webpack-plugin');

module.exports = [{
    context: path.join(__dirname, 'ecssercise/src'),
    entry: {
        style: "./scss/main.scss"
    },
    output: {
        path: path.join(__dirname, '/ecssercise/static/css'),
        filename: '[name].css'
    },
    module: {
        loaders: [
        {
            test: /\.scss$/,
            loader: ExtractTextPlugin.extract({
                use: ['css-loader', 'sass-loader'],
                fallback: 'style-loader',
            })
        }
        ]
    },
    plugins: [
        new ExtractTextPlugin('[name].css')
    ]
}];
