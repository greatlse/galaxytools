#!/usr/bin/env python
import argparse
import subprocess
import tempfile
import imagej2_base_utils

# Parse Command Line.
parser = argparse.ArgumentParser()
parser.add_argument( '--source_image', dest='source_image', help='Source image' )
parser.add_argument( '--source_image_format', dest='source_image_format', help='Source image format' )
parser.add_argument( '--target_image', dest='target_image', help='Target image' )
parser.add_argument( '--target_image_format', dest='target_image_format', help='Target image format' )
parser.add_argument( '--source_elastic_transformation', dest='source_elastic_transformation', help='Direct source transformation matrix' )
parser.add_argument( '--target_elastic_transformation', dest='target_elastic_transformation', help='Inverse target transformation matrix' )
parser.add_argument( '--output', dest='output', help='Warping index' )

args = parser.parse_args()

tmp_dir = imagej2_base_utils.get_temp_dir()
source_image_path = imagej2_base_utils.get_input_image_path( tmp_dir, args.source_image, args.source_image_format )
target_image_path = imagej2_base_utils.get_input_image_path( tmp_dir, args.target_image, args.target_image_format )
source_elastic_transformation_path = imagej2_base_utils.get_input_image_path( tmp_dir, args.source_elastic_transformation, 'txt' )
target_elastic_transformation_path = imagej2_base_utils.get_input_image_path( tmp_dir, args.target_elastic_transformation, 'txt' )

# Define command response buffers.
tmp_out = tempfile.NamedTemporaryFile().name
tmp_stdout = open( tmp_out, 'wb' )
tmp_err = tempfile.NamedTemporaryFile().name
tmp_stderr = open( tmp_err, 'wb' )

# Build the command line to compose the transformations.
cmd = imagej2_base_utils.get_base_cmd_bunwarpj( None )
if cmd is None:
    imagej2_base_utils.stop_err( "bUnwarpJ not found!" )
cmd += ' -compose_elastic'
# Target is sent before source.
cmd += ' %s' % target_image_path
cmd += ' %s' % source_image_path
cmd += ' %s' % target_elastic_transformation_path
cmd += ' %s' % source_elastic_transformation_path
cmd += ' %s' % args.output

# Compose the two elastic transformations into a raw transformation using bUnwarpJ.
proc = subprocess.Popen( args=cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True )
rc = proc.wait()
if rc != 0:
    error_message = imagej2_base_utils.get_stderr_exception( tmp_err, tmp_stderr, tmp_out, tmp_stdout )
    imagej2_base_utils.stop_err( error_message )

imagej2_base_utils.cleanup_before_exit( tmp_dir )
