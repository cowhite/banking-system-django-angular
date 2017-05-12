module.exports = function(grunt) {
    grunt.loadNpmTasks('grunt-contrib-sass');
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.renameTask('concat', 'concatsass');
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-cssmin');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-karma');
    grunt.loadNpmTasks('grunt-bower-concat');


    grunt.initConfig({

        concatsass:{
            sass: {
                src: [
                    'app.sass',
                    'myapps/*.sass',
                    'myapps/*/*.sass',
                    'myapps/*/*/*.sass'
                ],
                dest: 'css/app.sass'
            }
        },

        sass: {
            compile: {
                files: {
                    'css/app.css': 'css/app.sass'
                }
            }
        },


        bower_concat: {
            all: {
                dest: {
                    js: 'bower_components/vendor.js',
                    css: 'bower_components/style.css'
                },
                mainFiles: {
                    'angular-ui-router': ['release/angular-ui-router.js'],
                    'angular-datatables': ['bundles/angular-datatables.umd.js']
                },

                dependencies: {
                    'angular-material': 'angular-ui-router'
                },
                exclude:[
                ]

            }
        },

        concat: {
            css: {
                src: [
                    'bower_components/angular-material/angular-material.min.css',
                    'css/app.css'
                ],
                dest: 'dist/app.css'
            },
            libjs: {
                src: [
                    'bower_components/jquery/dist/jquery.js',
                    'bower_components/datatables/media/js/jquery.dataTables.js',
                    'bower_components/angular/angular.js',
                    'bower_components/angular-ui-router/release/angular-ui-router.js',
                    'node_modules/angular-ui-bootstrap/dist/ui-bootstrap.js',
                    'bower_components/angular-animate/angular-animate.min.js',
                    'bower_components/angular-aria/angular-aria.min.js',
                    'bower_components/angular-messages/angular-messages.min.js',
                    'bower_components/angular-material/angular-material.min.js',
                    'bower_components/ngstorage/ngStorage.min.js',
                    'bower_components/angular-sanitize/angular-sanitize.min.js',
                    'bower_components/angular-svg-round-progressbar/build/roundProgress.js',
                    'bower_components/angular-datatables/bundles/angular-datatables.umd.js'

                ],
                dest: 'dist/vendor.js'
            },
            appjs: {
                src: [
                    'app.js',
                    'myapps/*.js',
                    'myapps/*/*.js',
                    'myapps/*/*/*.js',
                    '!Gruntfile.js'
                ],
                dest: 'dist/app.js'
            },
        },
        cssmin: {
            options: {
                shorthandandCompacting: false,
                roundingPrecision: -1
            },
            target: {
                files: {
                    'dist/app.min.css': [
                        'dist/app.css'
                    ]
                }
            }
        },

        uglify: {
            js: {
                files: {
                    'dist/app.min.js': [
                        'dist/vendor.js',
                        'dist/app.js'
                    ]
                }
            }
        },

        watch : {
            sass: {
                files: ['main/static/css/**/*.sass'],
                tasks: ['sass']
            },
            css: {
                files: ['main/static/css/**/*.css'],
                tasks: ['concat:css']
            },
            appjs: {
                files: ['main/static/js/**/*.js', 'app/**/*.js'],
                tasks: ['concat:appjs', 'karma']
            },
            libjs: {
                files: ['main/static/lib/**/*.js'],
                tasks: ['concat:libjs', 'karma']
            },
        },
        karma: {
            unit: {
                configFile: 'karma.conf.js',
                singleRun: true
            }
        }
    });
    grunt.registerTask('default', [
        'concatsass',
        'sass',
        'concat',
        'karma',
        'watch'
    ]);

    grunt.registerTask('nowatch', [
        'concatsass',
        'sass',
        'concat',
        'karma'
    ]);

    grunt.registerTask('minify', [
        'concatsass',
        'sass',
        // 'bower_concat',
        'concat',
        'cssmin',
        //'uglify'
    ]);
};
