
LANGUAGE_NAMES = (
    ("py", "Python 2 (.py)"),
    ("py3", "Python 3 (.py)"),
    ("pl", "Perl (.pl)"),
    ("java", "Java (.java)"),
    ("c", "C [code] (.c)"),
    ("h", "C [header] (.h)"),
    ("cpp", "C++ [code] (.cpp)"),
    ("hpp", "C++ [header] (.hpp)"),
    ("js", "Javascript (.js)"),
    ("css", "CSS (.css)"),
    ("html", "HTML (.html)"),
    ("php", "PHP (.php)"),
    ("rb", "Ruby (.rb)"),
    ("sh", "Shell Script (.sh)"),
    ("go", "Go (.go)"),
    ("hs", "Haskell (.hs)")
)

EDITOR_LANGUAGES = {
    'py' : {'ace' : "python", 'code' : "print 'Hola Mundo'", 'lang': "Python 2"},
    'py3': {'ace' : "python", 'code' : "print('Hola Mundo')", 'lang': "Python 3"},
    'pl': {'ace' : "perl", 'code' : "", 'lang': "Perl"},
    'java': {'ace' : "java", 'code' : '''
    public class HelloWorld {
        public static void main(String[] args) {
            System.out.println("Hola Mundo");
        }
    }
    ''', 'lang': "Java"},
    'c': {'ace' : "c_cpp", 'code' : '''
    #include <stdio.h>

    int main(int argc, char* argv[]) {
        printf("Hola Mundo");
    }
    ''', 'lang': "C [code]"},
    'h': {'ace' : "c_cpp", 'code' : '''
    #ifndef _HOLA_H_
    #define _HOLA_H_

    #endif
    ''', 'lang':  "C [header]"},
    'cpp': {'ace' : "c_cpp", 'code' : '''
    ''', 'lang': "C++ [code]"},
    'hpp': {'ace' : "c_cpp", 'code' : '''
    ''', 'lang': "C++ [header]"},
    'js': {'ace' : "javascript", 'code' : '''
    alert('Hola Mundo');
    ''', 'lang': "Javascript"},
    'css': {'ace' : "css", 'code' : '''
    body {
    }
    ''', 'lang': "CSS"},
    'html': {'ace' : "css", 'code' : '''
    <html>
        <body>
            <h1>Hola Mundo</h1>
        </body>
    </html>
    ''', 'lang': "HTML"},
    'php': {'ace' : "php", 'code' : '''
    <?php
        echo "Hola Mundo";
    ?>
    ''', 'lang': "PHP"},
    'rb': {'ace' : "ruby", 'code' : '''
    ''', 'lang': "Ruby"},
    'sh': {'ace' : "sh", 'code' : '''
    #! /bin/sh

    echo 'Hola Mundo'
    ''', 'lang': "Shell Script"},
    'go': {'ace' : "golang", 'code' : '''
    ''', 'lang': "Go"},
    'hs': {'ace' : "haskell", 'code' : '''
    ''', 'lang': "Haskell"},
}
