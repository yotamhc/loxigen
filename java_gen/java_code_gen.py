import of_g
from loxi_ir import *
import pdb
import os
import shutil

import lang_java

import loxi_utils.loxi_utils as loxi_utils

import java_gen.msgs as msgs
import java_gen.java_utils as java_utils

def gen_java_interfaces():
    of_classes_per_version = {}
    for wire_version, of_protocol in of_g.ir.items():
        java_version = JavaOFVersion(wire_version)

        for of_class in of_protocol.classes:
            of_classes[of_class.name][java_version] = of_class

def gen_all_java(out, name):
    target_dir='loxi_output/openflowj'
    basedir="%s/%s/" % (
            target_dir,
            lang_java.file_to_subdir_map['base_java'])
    srcdir = "%s/src/main/java/" % basedir
    print "Outputting to %s" % basedir
    if os.path.exists(basedir):
        shutil.rmtree(basedir)
    os.makedirs(basedir)
    java_utils.copy_prewrite_tree(basedir)
    msgs.set_basedir(srcdir)
    msgs.create_message_interfaces()
    msgs.create_message_classes()
    msgs.create_of_const_enums()
    with open('README.java-lang') as readme_src:
        out.writelines(readme_src.readlines())
    out.close()
