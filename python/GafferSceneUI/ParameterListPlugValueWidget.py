##########################################################################
#  
#  Copyright (c) 2012, John Haddon. All rights reserved.
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

import IECore

import Gaffer
import GafferUI
import GafferScene

class ParameterListPlugValueWidget( GafferUI.CompoundPlugValueWidget ) :

	def __init__( self, plug, collapsible=True, **kw ) :

		GafferUI.CompoundPlugValueWidget.__init__( self, plug, collapsible, **kw )

		self.__footerWidget = None

	def _childPlugWidget( self, childPlug ) :
	
		row = GafferUI.ListContainer( GafferUI.ListContainer.Orientation.Horizontal, spacing = 4 )
		
		if False :
			## \todo We need a Locked or Settable flag for Plugs, then when they
			# are locked we can display them in static form.
			nameWidget = GafferUI.Label(
				childPlug["name"].getValue(),
				horizontalAlignment = GafferUI.Label.HorizontalAlignment.Right,
				verticalAlignment = GafferUI.Label.VerticalAlignment.Top,
			)
		else :
			nameWidget = GafferUI.PlugValueWidget.create( childPlug["name"] )
			
		## \todo This isn't working - maybe we need a FixedSizeContainer?
		nameWidget._qtWidget().setFixedWidth( GafferUI.PlugWidget.labelWidth() )
		row.append( nameWidget )
		
		row.append( GafferUI.PlugValueWidget.create( childPlug["value"] ) )
		
		return row
		
	def _footerWidget( self ) :
	
		if self.__footerWidget is not None :
			return self.__footerWidget
			
		self.__footerWidget = GafferUI.ListContainer( GafferUI.ListContainer.Orientation.Horizontal )
		self.__footerWidget.append( GafferUI.Spacer( IECore.V2i( GafferUI.PlugWidget.labelWidth(), 1 ) ) )
		self.__footerWidget.append(
			GafferUI.MenuButton( image="plus.png", hasFrame=False, menu=GafferUI.Menu( self.__addMenuDefinition() ) )
		)
		self.__footerWidget.append( GafferUI.Spacer( IECore.V2i( 1 ), IECore.V2i( 999999, 1 ) ), expand = True )

		return self.__footerWidget
			
	def __addMenuDefinition( self ) :
	
		result = IECore.MenuDefinition()
		result.append( "/Add/Float", { "command" : IECore.curry( Gaffer.WeakMethod( self.__addItem ), "", IECore.FloatData( 0 ) ) } )
		result.append( "/Add/Int", { "command" : IECore.curry( Gaffer.WeakMethod( self.__addItem ), "", IECore.IntData( 0 ) ) } )
		result.append( "/Add/String", { "command" : IECore.curry( Gaffer.WeakMethod( self.__addItem ), "", IECore.StringData( "" ) ) } )
		
		return result
		
	def __addItem( self, name, value ) :
	
		self.getPlug().addParameter( name, value )
		
GafferUI.PlugValueWidget.registerType( GafferScene.ParameterListPlug.staticTypeId(), ParameterListPlugValueWidget )
