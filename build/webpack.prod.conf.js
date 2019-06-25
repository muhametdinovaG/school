'use strict'
process.env.NODE_ENV = 'production'

const webpack = require('webpack')
const config = require('../configs')
const merge = require('webpack-merge')
const CleanWebpackPlugin = require('clean-webpack-plugin')
const BundleTracker = require('webpack-bundle-tracker')
const baseWebpackConfig = require('./webpack.base.conf')
const ExtractTextPlugin = require('extract-text-webpack-plugin')

module.exports = merge(baseWebpackConfig, {
    mode: 'production',
    devtool: config.build.productionSourceMap ? config.build.devtool : false,
    module: {
        rules: [
            {
                test: /\.(sa|sc|c)ss$/,
                use: ExtractTextPlugin.extract({
                    fallback: 'style-loader',
                    use: [ 'css-loader', 'postcss-loader', 'sass-loader' ]
                })
            }
        ]
    },
    plugins: [
        new CleanWebpackPlugin(['dist'], { root: '/home/app_utvschool/utv_school/'}),
        new BundleTracker({filename: 'dist/webpack-stats-prod.json'}),
        new webpack.NoEmitOnErrorsPlugin(),
        new ExtractTextPlugin({
          filename: 'css/style.css'
        })
    ]
});