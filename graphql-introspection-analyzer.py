#!/usr/bin/python2

import sys
import os
import json
from termcolor import colored
from operator import attrgetter



class GraphqlObject:
    name = ""
    ttype = ""
    args = []
    attrs = []
    values = []
    inputs = []

    def __init__( self ):
        self.args = []
        self.attrs = []
        self.values = []
        self.inputs = []

class GraphqlAttribut:
    name = ""
    ttype = ""

class GraphqlArgument:
    name = ""
    ttype = ""

class GraphqlValue:
    name = ""


def usage( err='' ):
    print( "1/ First step is to run the introspection query on the server, and store the JSON returned in a file.\n")
    print( "GET:")
    print( "/graphql?query={__schema{queryType{name},mutationType{name},subscriptionType{name},types{...FullType},directives{name,description,locations,args{...InputValue}}}},fragment%20FullType%20on%20__Type{kind,name,description,fields(includeDeprecated:true){name,description,args{...InputValue},type{...TypeRef},isDeprecated,deprecationReason},inputFields{...InputValue},interfaces{...TypeRef},enumValues(includeDeprecated:true){name,description,isDeprecated,deprecationReason},possibleTypes{...TypeRef}},fragment%20InputValue%20on%20__InputValue{name,description,type{...TypeRef},defaultValue},fragment%20TypeRef%20on%20__Type{kind,name,ofType{kind,name,ofType{kind,name,ofType{kind,name,ofType{kind,name,ofType{kind,name,ofType{kind,name,ofType{kind,name}}}}}}}}\n")
    print( "POST:")
    print( '{"query":"{__schema{queryType{name},mutationType{name},subscriptionType{name},types{...FullType},directives{name,description,locations,args{...InputValue}}}},fragment FullType on __Type{kind,name,description,fields(includeDeprecated:true){name,description,args{...InputValue},type{...TypeRef},isDeprecated,deprecationReason},inputFields{...InputValue},interfaces{...TypeRef},enumValues(includeDeprecated:true){name,description,isDeprecated,deprecationReason},possibleTypes{...TypeRef}},fragment InputValue on __InputValue{name,description,type{...TypeRef},defaultValue},fragment TypeRef on __Type{kind,name,ofType{kind,name,ofType{kind,name,ofType{kind,name,ofType{kind,name,ofType{kind,name,ofType{kind,name,ofType{kind,name}}}}}}}}","variables":{}}\n')
    print( "2/ Then run this program.\n")
    print( "Usage: %s <introspection file>" % sys.argv[0] )
    if err:
        print( "Error: %s!" % err )
    print("")
    sys.exit()


def displayTypeO( o ):
    sys.stdout.write( colored("%s" % o.ttype, t_colors[o.ttype] if o.ttype in t_colors else default_color ) )
    sys.stdout.write( " %s {\n" % o.name )

    if len(o.attrs):
        l = sorted( o.attrs, key=lambda w:attrgetter('name')(w).lower() )
        for elt in l:
            sys.stdout.write( "  %s" % elt.name )
            sys.stdout.write( colored(" %s" % elt.ttype, 'white') )
            if not elt == l[-1]:
                sys.stdout.write( "," )
            sys.stdout.write( "\n" )
    if len(o.inputs):
        l = sorted( o.inputs, key=lambda w:attrgetter('name')(w).lower() )
        for elt in l:
            sys.stdout.write( "  %s" % elt.name )
            sys.stdout.write( colored(" %s" % elt.ttype, 'white') )
            if not elt == l[-1]:
                sys.stdout.write( "," )
            sys.stdout.write( "\n" )
    if len(o.values):
        l = sorted( o.values, key=lambda w:attrgetter('name')(w).lower() )
        for elt in l:
            sys.stdout.write( "  %s" % elt.name )
            if not elt == l[-1]:
                sys.stdout.write( "," )
            sys.stdout.write( "\n" )

    sys.stdout.write( "}\n\n" )


def displayTypeQM( o ):
    sys.stdout.write( colored("%s" % o.ttype, t_colors[o.ttype] if o.ttype in t_colors else default_color ) )
    sys.stdout.write( " %s (\n" % o.name )

    if len(o.args):
        l = sorted( o.args, key=lambda w:attrgetter('name')(w).lower() )
        for elt in l:
            sys.stdout.write( "  %s" % elt.name )
            sys.stdout.write( colored(" %s" % elt.ttype, 'white') )
            if not elt == l[-1]:
                sys.stdout.write( "," )
            sys.stdout.write( "\n" )

    sys.stdout.write( ")\n\n" )


# this is a list
t_keywords = [
    'Query','Mutation',
    'Boolean','String','ID','Float','Int',
    '__Schema','__Type','__Field','__Directive','__EnumValue','__InputValue','__TypeKind','__DirectiveLocation'
]

# this is a dict
t_colors = {
    'QUERY': 'cyan',
    'MUTATION': 'red',
    'ENUM': 'yellow',
    'INTERFACE': 'blue',
};

default_color = 'green'

t_objects = [];
t_queries = [];
t_mutations = [];


if len(sys.argv) != 2:
    usage( 'introspection file not found' )

ifile = sys.argv[1]

if not os.path.isfile(ifile):
    usage( 'introspection file not found' )

with open(ifile) as jfile:
    data = json.load( jfile )
    for v in data['data']['__schema']['types']:
        if v['name'] == 'Query' or v['name'] == 'Mutation':
            if 'fields' in v and type(v['fields']) is list and len(v['fields'])>0:
                for vv in v['fields']:
                    o = GraphqlObject()
                    o.name = vv['name']
                    o.ttype = 'QUERY' if v['name'] == 'Query' else 'MUTATION';

                    if 'args' in vv and type(vv['args']) is list and len(vv['args'])>0:
                        for vvv in vv['args']:
                            if vvv['type']['name']:
                                ttype = vvv['type']['name']
                            elif vvv['type']['ofType']['name']:
                                ttype = vvv['type']['ofType']['name']
                            elif vvv['type']['ofType']['ofType']['name']:
                                ttype = vvv['type']['ofType']['ofType']['name']
                            elif vvv['type']['ofType']['ofType']['ofType']['name']:
                                ttype = vvv['type']['ofType']['ofType']['ofType']['name']
                            arg = GraphqlArgument()
                            arg.name = vvv['name']
                            arg.ttype = ttype
                            o.args.append( arg )

                    if o.ttype == 'QUERY':
                        t_queries.append( o )
                    else:
                        t_mutations.append( o )
        else:
            if v['name'] in t_keywords:
                continue

            o = GraphqlObject()
            o.name = v['name']
            o.ttype = v['kind']

            if 'fields' in v and type(v['fields']) is list and len(v['fields'])>0:
                for vv in v['fields']:
                    if vv['type']['name']:
                        ttype = vv['type']['name']
                    elif vv['type']['ofType']['name']:
                        ttype = vv['type']['ofType']['name']
                    elif vv['type']['ofType']['ofType']['name']:
                        ttype = vv['type']['ofType']['ofType']['name']
                    elif vv['type']['ofType']['ofType']['ofType']['name']:
                        ttype = vv['type']['ofType']['ofType']['ofType']['name']
                    attr = GraphqlAttribut()
                    attr.name = vv['name']
                    attr.ttype = ttype
                    o.attrs.append( attr )

            if 'inputFields' in v and type(v['inputFields']) is list and len(v['inputFields'])>0:
                for vv in v['inputFields']:
                    if vv['type']['name']:
                        ttype = vv['type']['name']
                    elif vv['type']['ofType']['name']:
                        ttype = vv['type']['ofType']['name']
                    elif vv['type']['ofType']['ofType']['name']:
                        ttype = vv['type']['ofType']['ofType']['name']
                    elif vv['type']['ofType']['ofType']['ofType']['name']:
                        ttype = vv['type']['ofType']['ofType']['ofType']['name']
                    i = GraphqlAttribut()
                    i.name = vv['name']
                    i.ttype = ttype
                    o.inputs.append( i )

            if 'enumValues' in v and type(v['enumValues']) is list and len(v['enumValues'])>0:
                for vv in v['enumValues']:
                    value = GraphqlValue()
                    value.name = vv['name']
                    o.values.append( value )

            t_objects.append( o );

if len(t_objects):
    l = sorted( t_objects, key=lambda w:attrgetter('name')(w).lower() )
    for o in l:
        displayTypeO( o )

if len(t_queries):
    l = sorted( t_queries, key=lambda w:attrgetter('name')(w).lower() )
    for q in l:
        displayTypeQM( q )

if len(t_mutations):
    l = sorted( t_mutations, key=lambda w:attrgetter('name')(w).lower() )
    for m in l:
        displayTypeQM( m )