import os, io
import zipfile


JAVA_VERSIONS = {45: '1.1',
                 46: '1.2',
                 47: '1.3',
                 48: '1.4',
                 49: '5',
                 50: '6',
                 51: '7',
                 52: '8'}


def extract_java_version(bytes):
    _h, _l = bytes[6:8]
    v = (_h << 8) + _l
    return JAVA_VERSIONS.get(v, 'Unknown')


def get_java_version_from_class(classfile):
    with open(classfile, 'rb') as file:
        bytes = file.read(10)
        return extract_java_version(bytes)


def get_java_version_from_archive(arc):
    found_versions = set()
    for name in arc.namelist():
        if name.endswith('.class'):
            file = arc.open(name)
            data = file.read(10)
            found_versions.add(extract_java_version(data))
        elif name.endswith('.jar') or name.endswith('.war'):
            zfiledata = io.BytesIO(arc.read(name))
            jar = zipfile.ZipFile(zfiledata)
            found_versions.update(get_java_version_from_archive(jar))
    return found_versions


def print_java_version_of_files_in(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            filepath = os.path.join(root, file)
            if file.endswith('.class'):
                version = get_java_version_from_class(filepath)
            elif file.endswith('.jar') or file.endswith('.war'):
                arc = zipfile.ZipFile(filepath)
                version = get_java_version_from_archive(arc)
            else:
                continue
            ver_str = ', '.join(sorted(version))
            print('{:30s} {}'.format(ver_str, filepath))



if __name__ == '__main__':
    path = 'path/to/jar_war_classes'
    print_java_version_of_files_in(path)

