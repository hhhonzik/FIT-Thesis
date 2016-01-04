module.exports = function (grunt) {
    "use strict";

    var minify = grunt.option('minify') === undefined || grunt.option('minify') === true;

    grunt.option('transform', minify ? 'uglifyify' : '');

    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        browserify: {
            dist: {
                files: {
                    'dist/jquery.html5anim.min.js': ['src/jquery.html5anim.js']
                },
                options: {
                    debug: false,
                    transform: [grunt.option('transform')]
                }
            },
            dev: {
                files: {
                    'dist/jquery.html5anim.js': ['src/jquery.html5anim.js']
                },
                options: {
                    debug: true
                }
            }
        },
        jslint: {
            frontend: {
                src: [
                    'Gruntfile.js',
                    'src/app/**/*.js'
                ],
                directives: {
                    browser: true,
                    nomen: true,
                    predef: [
                        'jQuery',
                        'module',
                        'require',
                        'console',
                        '$'
                    ]
                },
                options: {
                    failOnError: false,
                    errorsOnly: true
                }
            }
        },
        watch: {
            js: {
                files: ['src/**/*.js'],
                tasks: ['jslint:frontend', 'browserify']
            }
        },
        mochaTest: {
            test: {
                src: ['test/**/*.js']
            }
        }
    });

    grunt.loadNpmTasks('grunt-browserify');
    grunt.loadNpmTasks('grunt-jslint');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-mocha-test');


    grunt.registerTask('default', [
        'browserify',
        'jslint',
        'watch'
    ]);
    grunt.registerTask('test', ['mochaTest']);
};