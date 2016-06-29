import React from 'react';


var ContentList = React.createClass({
    render: function() {
        return <div className="container">
            {this.props.threads.map((i) => 
                <div className="row" key={i.link}><a href="{i.link}">{i.title}</a></div>)}
        </div>
    }
});

var test_list = [
    {link: 'hello', title: 'aeraddas'} ,
    {link: 'hello2', title: 'aeraddas'} 
    ];

export default React.createClass({
    getInitialState: function() {
        this.getCurrentThreads();
        return {'items': []};
    },
    getCurrentThreads: function() {
        $.ajax({
            url: '/api/post',
            success: function(result) {
                this.setState({'items': result});
            }.bind(this)
        });
    },
    render: function() { 
        return <ContentList threads={this.state.items} />;
    }
});
