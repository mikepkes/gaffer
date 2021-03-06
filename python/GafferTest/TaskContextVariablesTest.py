##########################################################################
#
#  Copyright (c) 2015, Image Engine Design Inc. All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#
#      * Redistributions of source code must retain the above
#        copyright notice, this list of conditions and the following
#        disclaimer.
#
#      * Redistributions in binary form must reproduce the above
#        copyright notice, this list of conditions and the following
#        disclaimer in the documentation and/or other materials provided with
#        the distribution.
#
#      * Neither the name of John Haddon nor the names of
#        any other contributors to this software may be used to endorse or
#        promote products derived from this software without specific prior
#        written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
#  IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
#  THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
#  PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
#  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
##########################################################################

import glob
import unittest

import Gaffer
import GafferTest

class TaskContextVariablesTest( GafferTest.TestCase ) :

	def __dispatcher( self, frameRange = None ) :

		result = Gaffer.LocalDispatcher( jobPool = Gaffer.LocalDispatcher.JobPool() )
		result["jobsDirectory"].setValue( self.temporaryDirectory() + "/jobs" )

		return result

	def test( self ) :

		script = Gaffer.ScriptNode()

		script["writer"] = GafferTest.TextWriter()
		script["writer"]["fileName"].setValue( self.temporaryDirectory() + "/${name}.txt" )

		script["variables"] = Gaffer.TaskContextVariables()
		script["variables"]["requirements"][0].setInput( script["writer"]["requirement"] )
		script["variables"]["variables"].addMember( "name", "jimbob" )

		self.__dispatcher().dispatch( [ script["variables"] ] )

		self.assertEqual(
			set( glob.glob( self.temporaryDirectory() + "/*.txt" ) ),
			{
				self.temporaryDirectory() + "/jimbob.txt",

			}
		)

	def testDisabledVariable( self ) :

		script = Gaffer.ScriptNode()

		script["writer"] = GafferTest.TextWriter()
		script["writer"]["fileName"].setValue( self.temporaryDirectory() + "/${name1}${name2}.txt" )

		script["variables"] = Gaffer.TaskContextVariables()
		script["variables"]["requirements"][0].setInput( script["writer"]["requirement"] )
		jim = script["variables"]["variables"].addOptionalMember( "name1", "jim", enabled = False )
		bob = script["variables"]["variables"].addOptionalMember( "name2", "bob", enabled = True )

		self.__dispatcher().dispatch( [ script["variables"] ] )

		self.assertEqual(
			set( glob.glob( self.temporaryDirectory() + "/*.txt" ) ),
			{
				self.temporaryDirectory() + "/bob.txt",

			}
		)

	def testBackgroundDispatch( self ) :

		script = Gaffer.ScriptNode()

		script["writer"] = GafferTest.TextWriter()
		script["writer"]["fileName"].setValue( self.temporaryDirectory() + "/${name}.txt" )

		script["variables"] = Gaffer.TaskContextVariables()
		script["variables"]["requirements"][0].setInput( script["writer"]["requirement"] )
		script["variables"]["variables"].addMember( "name", "jimbob" )

		dispatcher = self.__dispatcher()
		dispatcher["executeInBackground"].setValue( True )
		dispatcher.dispatch( [ script["variables"] ] )

		dispatcher.jobPool().waitForAll()
		self.assertEqual( len( dispatcher.jobPool().failedJobs() ), 0 )

		self.assertEqual(
			set( glob.glob( self.temporaryDirectory() + "/*.txt" ) ),
			{
				self.temporaryDirectory() + "/jimbob.txt",
			}
		)

if __name__ == "__main__":
	unittest.main()
