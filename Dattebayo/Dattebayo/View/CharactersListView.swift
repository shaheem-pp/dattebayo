//
//  HomeView.swift
//  Dattebayo
//
//  Created by Shaheem PP on 12/09/2024.
//

import SwiftUI

struct CharactersListView: View {
    @StateObject private var viewModel = CharactersViewModel()
    
    var body: some View {
        NavigationView {
            VStack {
                if viewModel.characters.isEmpty {
                    Text("Loading characters...")
                } else {
                    List(viewModel.characters, id: \.id) { character in
                        NavigationLink(destination: CharacterDetailView(character: character)) {
                            VStack(alignment: .leading) {
                                Rectangle()
                                    .frame(width: 300, height: 300)
                                    .background(Color.green)
                                Text(character.name ?? "Name")
                                    .font(.headline)
                            }
                            .padding()
                        }
                    }
                }
            }
            .task {
                await viewModel.loadData()
            }
            .navigationTitle("Characters List")
        }
    }
}

struct CharacterDetailView: View {
    let character: Character
    
    var body: some View {
        VStack {
            Text(character.name ?? "Unknown")
                .font(.largeTitle)
                .padding()            
        }
        .navigationTitle(character.name ?? "Character Detail")
    }
}

struct CharactersListView_Previews: PreviewProvider {
    static var previews: some View {
        CharactersListView()
    }
}
