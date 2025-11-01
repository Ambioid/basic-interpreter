project(
    'basic-interpreter',
    'cpp',
    default_options: [
        'warning_level=3',
        'cpp_std=c++20',
    ],
)

cc = meson.get_compiler('cpp')
m_dep = cc.find_library('m', required: false)

executable(
    'basic-interpreter',
    sources: [
        'src/main.cpp',
    ],
    dependencies: m_dep,
)
