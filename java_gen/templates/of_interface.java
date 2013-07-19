//:: # Copyright 2013, Big Switch Networks, Inc.
//:: #
//:: # LoxiGen is licensed under the Eclipse Public License, version 1.0 (EPL), with
//:: # the following special exception:
//:: #
//:: # LOXI Exception
//:: #
//:: # As a special exception to the terms of the EPL, you may distribute libraries
//:: # generated by LoxiGen (LoxiGen Libraries) under the terms of your choice, provided
//:: # that copyright and licensing notices generated by LoxiGen are not altered or removed
//:: # from the LoxiGen Libraries and the notice provided below is (i) included in
//:: # the LoxiGen Libraries, if distributed in source code form and (ii) included in any
//:: # documentation for the LoxiGen Libraries, if distributed in binary form.
//:: #
//:: # Notice: "Copyright 2013, Big Switch Networks, Inc. This library was generated by the LoxiGen Compiler."
//:: #
//:: # You may not use this file except in compliance with the EPL or LOXI Exception. You may obtain
//:: # a copy of the EPL at:
//:: #
//:: # http::: #www.eclipse.org/legal/epl-v10.html
//:: #
//:: # Unless required by applicable law or agreed to in writing, software
//:: # distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
//:: # WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
//:: # EPL for the specific language governing permissions and limitations
//:: # under the EPL.
//::
//:: import itertools
//:: import of_g
//:: include('_copyright.java')

//:: include('_autogen.java')

package ${msg.package};

//:: include("_imports.java", msg=msg)

public interface ${msg.name} ${"extends %s" % msg.parent_interface if msg.parent_interface else ""} {
//:: for prop in (prop for prop in msg.members):
    ${prop.java_type.public_type} get${prop.title_name}()${ "" if prop.is_universal else " throws UnsupportedOperationException"};
//:: #endfor

    int writeTo(ChannelBuffer channelBuffer);

    Builder createBuilder();
    public interface Builder ${"extends %s.Builder" % msg.parent_interface if msg.parent_interface else ""} {
        ${msg.name} getMessage();
//:: for prop in msg.members:
        ${prop.java_type.public_type} get${prop.title_name}()${ "" if prop.is_universal else " throws UnsupportedOperationException"};
//:: if prop.is_writeable:
        Builder set${prop.title_name}(${prop.java_type.public_type} ${prop.name})${ "" if prop.is_universal else " throws UnsupportedOperationException"};
//:: #endif
//:: #endfor

    }
}