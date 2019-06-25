'use strict'
process.env.NODE_ENV = 'development'

const webpack = require('webpack')
const config = require('../configs')
const merge = require('webpack-merge')
const BundleTracker = require('webpack-bundle-tracker')
const baseWebpackConfig = require('./webpack.base.conf')

module.exports = merge(baseWebpackConfig, {
    mode: 'development',
    devtool: config.dev.devtool,
    devServer: {
        compress: true,
        open: config.dev.autoOpenBrowser,
        overlay: config.dev.errorOverlay ? { warnings: false, errors: true } : false,
        publicPath: config.dev.assetsPublicPath,
        watchOptions: {
            poll: config.dev.poll
        },
        headers: {
            'Access-Control-Allow-Origin': '*'
        }
    },
    optimization: {
        noEmitOnErrors: true
    },
    module: {
        rules: [
            {
                test: /\.(sa|sc|c)ss$/,
                use: [ 'style-loader', 'css-loader', 'postcss-loader', 'sass-loader' ]
            }
        ]
    },
    plugins: [
        new webpack.NoEmitOnErrorsPlugin(),
        new BundleTracker({
            filename: 'webpack-stats.json'
        })
    ]
});