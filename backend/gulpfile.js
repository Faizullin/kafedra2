var gulp = require('gulp');
var sass = require('gulp-sass')(require('sass'));
var del = require('del');
var sourcemaps = require('gulp-sourcemaps');
var uglify = require('gulp-uglify');
var cssmin = require('gulp-cssmin');
var merge = require('merge-stream');
var babel = require('gulp-babel');
var npmlodash = require('lodash');
var smushit = require('gulp-smushit');
var autoprefixer = require('gulp-autoprefixer');
var fileinclude = require('gulp-file-include');
var browsersync = require('browser-sync');
var htmlmin = require('gulp-htmlmin');
const {parallel} = require('gulp');

// Define multiple static sources
const static_src_paths = [
    'lms/static_src',  // Original source
    'static_src' // Additional static source
];

const dest_path = 'static';

// Function to create paths dynamically for multiple sources
const generatePaths = (srcPaths) => {
    return {
        src: {
            css: srcPaths.map(src => `${src}/assets/scss/*.scss`),
            layoutjs: srcPaths.map(src => `${src}/assets/js/*.js`),
            pagesjs: srcPaths.map(src => `${src}/assets/js/pages/*.js`),
            images: srcPaths.map(src => `${src}/assets/images/**/*.{jpg,png}`),
            dj_html: ['templates/**/*.html'] // Watch Django template changes
        },
        destination: {
            css: `${dest_path}/assets/css`,
            layoutjs: `${dest_path}/assets/js`,
            pagesjs: `${dest_path}/assets/js/pages`,
            images: `${dest_path}/assets/images`
        }
    };
};

const path = generatePaths(static_src_paths);

gulp.task('cleandist', function (callback) {
    del.sync([`${dest_path}/assets/*/`]);
    callback();
});

gulp.task('sass', function () {
    return gulp
        .src(path.src.css)
        .pipe(sourcemaps.init())
        .pipe(sass())
        .pipe(autoprefixer())
        .pipe(sourcemaps.write())
        .pipe(gulp.dest(path.destination.css));
});

gulp.task('build-node-modules', function () {
    var required_libs = {
        js: [
            'node_modules/bootstrap/dist/js/bootstrap.min.js',
            'node_modules/@popperjs/core/dist/umd/popper.min.js',
            'node_modules/simplebar/dist/simplebar.min.js',
            'node_modules/feather-icons/dist/feather.min.js',
            'node_modules/clipboard/dist/clipboard.min.js',
            'node_modules/apexcharts/dist/apexcharts.min.js',
        ],
        css: [
            'node_modules/bootstrap/dist/css/bootstrap.min.css',
        ]
    };

    npmlodash(required_libs).forEach(function (assets, type) {
        if (type === 'css') {
            gulp.src(assets).pipe(gulp.dest(`${dest_path}/assets/css/plugins`));
        } else {
            gulp.src(assets).pipe(gulp.dest(`${dest_path}/assets/js/plugins`));
        }
    });

    var cpyassets = merge(
        ...static_src_paths.map(src =>
            gulp.src([`${src}/assets/**/*.*`, `!${src}/assets/scss/**/*.*`]).pipe(gulp.dest(`${dest_path}/assets`))
        )
    );

    return cpyassets;
});

gulp.task('build-js', function () {
    var layoutjs = merge(...path.src.layoutjs.map(src => gulp.src(src).pipe(gulp.dest(path.destination.layoutjs))));
    var pagesjs = merge(...path.src.pagesjs.map(src => gulp.src(src).pipe(gulp.dest(path.destination.pagesjs))));
    return merge(layoutjs, pagesjs);
});

// Start BrowserSync and watch files
gulp.task('watch', function () {
    browsersync.init({
        proxy: "localhost:8000", // Change if your Django dev server runs on a different port
        notify: false,
        open: false
    });

    static_src_paths.forEach(src => {
        gulp.watch(`${src}/assets/scss/**/*.scss`, gulp.series('sass'));
        gulp.watch(`${src}/assets/js/**/*.js`, gulp.series('build-js')).on('change', browsersync.reload);
    });

    gulp.watch(path.src.dj_html).on('change', browsersync.reload);
});

gulp.task('min-css', function () {
    return gulp
        .src(path.src.css)
        .pipe(sass())
        .pipe(autoprefixer())
        .pipe(cssmin())
        .pipe(gulp.dest(path.destination.css));
});

gulp.task('min-js', function () {
    var layoutjs = merge(...path.src.layoutjs.map(src => gulp.src(src).pipe(uglify()).pipe(gulp.dest(path.destination.layoutjs))));
    var pagesjs = merge(...path.src.pagesjs.map(src => gulp.src(src).pipe(babel()).pipe(uglify()).pipe(gulp.dest(path.destination.pagesjs))));
    return merge(layoutjs, pagesjs);
});

function compressImagesWithRetry(src, dest, retries = 40) {
    return new Promise((resolve, reject) => {
        const stream = gulp
            .src(src)
            .pipe(smushit({verbose: true}))
            .on('error', function (err) {
                console.error('Error during image compression:', err.toString());
                if (retries > 0) {
                    compressImagesWithRetry(src, dest, retries - 1)
                        .then(resolve)
                        .catch(reject);
                } else {
                    reject(new Error('Max retries exceeded. Unable to compress image.'));
                }
            });

        stream.on('end', () => resolve());
        stream.pipe(gulp.dest(dest));
    });
}

gulp.task('min-image', function () {
    return compressImagesWithRetry(path.src.images, path.destination.images);
});

gulp.task('watch-minify', function () {
    static_src_paths.forEach(src => {
        gulp.watch(`${src}/assets/scss/**/*.scss`, gulp.series('min-css'));
        gulp.watch(`${src}/assets/js/**/*.js`, gulp.series('min-js'));
    });
});

gulp.task('build-prod', gulp.series('cleandist', 'build-node-modules', 'min-css', 'min-js'));
gulp.task('watch', gulp.series('cleandist',"build-node-modules", 'watch'));
