'use strict'

const path = require('path')
const config = require('../configs')

console.log(`building for ${process.env.NODE_ENV}...`)
module.exports = {
    context: path.resolve(__dirname, '../'),
    entry: {
        main: ['./modules/core/static/core/js/main.js']
    },
    output: {
        path: config.build.assetsRoot,
        filename: 'js/[name].js',
        publicPath: process.env.NODE_ENV === 'production' ? config.build.assetsPublicPath : config.dev.assetsPublicPath
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['env', 'stage-0']
                    }
                }
            },
            {
                test: /\.(png|svg|jpg)$/,
                use: {
                    loader: 'file-loader',
                    options: {
                        name: 'img/[name].[ext]'
                    }
                }
            },
            {
                test: /\.(woff|woff2|eot|ttf|otf)$/,
                use: {
                    loader: 'file-loader',
                    options: {
                        name: 'fonts/[name].[ext]'
                    }
                }
            }
        ]
    }
}