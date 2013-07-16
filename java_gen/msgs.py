import of_g
import os
import pdb
import re

import loxi_front_end.type_maps as type_maps
import loxi_utils.loxi_utils as utils
import py_gen.util as py_utils

import java_gen.java_utils as java_utils
from java_gen.java_model import *
ignore_fields = ['version', 'xid', 'length' ]

protected_fields = ['version', 'length']


templates_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates')
basedir = None

def set_basedir(pbasedir):
    global basedir
    basedir = pbasedir

def render_class(clazz, template, **context):
    context['class_name'] = clazz.name
    context['package'] = clazz.package

    filename = os.path.join(basedir, "%s/%s.java" % (clazz.package.replace(".", "/"), clazz.name))
    dirname = os.path.dirname(filename)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    prefix = '//::(?=[ \t]|$)'
    print "filename: %s" % filename
    with open(filename, "w") as f:
        utils.render_template(f, template, [templates_dir], context, prefix=prefix)

def create_of_const_enums():
    java_model = build_java_model()
    for enum in java_model.enums:
        if enum.name in ["OFPort"]:
            continue
        render_class(clazz=enum,
                template='const.java', enum=enum, all_versions=java_model.versions)

def create_message_interfaces():
    """ Create the base interfaces for of classes"""
    java_model = build_java_model()
    for interface in java_model.interfaces:
        #if not utils.class_is_message(interface.c_name):
        #    continue
        render_class(clazz=interface,
                template="message_interface.java", msg=interface)

def create_message_classes():
    java_model = build_java_model()
    """ Create the OF Messages for each version that implement the above interfaces"""
    for interface in java_model.interfaces:
        if not utils.class_is_message(interface.c_name) and not utils.class_is_action(interface.c_name):
            continue
        for java_class in interface.versioned_classes:
            render_class(clazz=java_class,
                    template='message_class.java', version=java_class.version, msg=java_class,
                    impl_class=java_class.name)

def create_action_interfaces(message_names):
    """ Create the base interfaces for Actions"""
    for msg_name in message_names:
        msg = JavaOFInterface(msg_name)
        render_class(class_name="org.openflow.protocol.action.%s" % msg.interface_name,
                    template='action_interface.java', msg=msg)


def create_action_classes(names):
    """ Create the OF Actions for each version that implement the above interfaces"""
    for msg_name in names:
        msg = JavaOFMessage(msg_name)
        for version in msg.all_versions():
            render_class(class_name="org.openflow.protocol.action.%s" % msg.class_name_for_version(version), template='action_class.java',
                     msg=msg, version=version, impl_class=msg.class_name_for_version(version))
